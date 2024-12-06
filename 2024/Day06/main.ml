open Core

let guard = '^'
let obstacle = '#'
let empty_space = '.'
let dirs = [| -1, 0; 0, 1; 1, 0; 0, -1 |]
let num_dirs = 4
let start_dir_id = 0

type state =
  { row : int
  ; col : int
  ; dir_id : int
  }

module State = struct
  module T = struct
    type t = state

    let compare t1 t2 =
      let cmp_row = Int.compare t1.row t2.row in
      if cmp_row <> 0
      then cmp_row
      else (
        let cmp_col = Int.compare t1.col t2.col in
        if cmp_col <> 0 then cmp_col else Int.compare t1.dir_id t2.dir_id)
    ;;

    let sexp_of_t t =
      Sexp.List [ Int.sexp_of_t t.row; Int.sexp_of_t t.col; Int.sexp_of_t t.dir_id ]
    ;;

    let move_forward { row; col; dir_id } =
      let dr, dc = dirs.(dir_id) in
      { row = row + dr; col = col + dc; dir_id }
    ;;

    let turn_right t = { t with dir_id = (t.dir_id + 1) % num_dirs }
  end

  include T
  include Comparator.Make (T)
end

let read () = Array.of_list_map ~f:String.to_array In_channel.(input_lines stdin)

let find_start =
  Array.find_mapi_exn ~f:(fun r row ->
    Array.findi ~f:(fun _ cell -> Char.equal cell guard) row
    |> Option.map ~f:(fun (c, _) -> r, c))
;;

let is_out_of_bounds grid row col =
  row < 0 || row >= Array.length grid || col < 0 || col >= Array.length grid.(0)
;;

let find_next_state grid state =
  let ({ row = new_row; col = new_col; _ } as forward_state) = State.move_forward state in
  if is_out_of_bounds grid new_row new_col
  then None
  else if Char.equal grid.(new_row).(new_col) obstacle
  then Some (State.turn_right state)
  else Some forward_state
;;

let blocking_creates_cycle grid blocked_row blocked_col start_state =
  let rec is_stuck_in_cycle states_seen state =
    match find_next_state grid state with
    | None -> false
    | Some next_state when Set.mem states_seen next_state -> true
    | Some next_state ->
      let new_states_seen = Set.add states_seen next_state in
      is_stuck_in_cycle new_states_seen next_state
  in
  grid.(blocked_row).(blocked_col) <- obstacle;
  let res = is_stuck_in_cycle (Set.empty (module State)) start_state in
  grid.(blocked_row).(blocked_col) <- empty_space;
  res
;;

let traverse_fold grid start_state ~init ~f =
  let height = Array.length grid in
  let width = Array.length grid.(0) in
  let pos_seen = Array.make_matrix ~dimx:height ~dimy:width false in
  let rec loop opt_prev_state curr_state acc =
    let is_new_pos = not pos_seen.(curr_state.row).(curr_state.col) in
    let new_acc = f acc opt_prev_state curr_state ~is_new_pos in
    pos_seen.(curr_state.row).(curr_state.col) <- true;
    let opt_next_state = find_next_state grid curr_state in
    match opt_next_state with
    | None -> new_acc
    | Some next_state -> loop (Some curr_state) next_state new_acc
  in
  loop None start_state init
;;

let solve_part1 =
  traverse_fold ~init:0 ~f:(fun total _ _ ~is_new_pos -> total + Bool.to_int is_new_pos)
;;

let solve_part2 grid =
  traverse_fold grid ~init:0 ~f:(fun total opt_prev_state curr_state ~is_new_pos ->
    (* When about to reach new position for first time, try blocking it to see if loop created *)
    match opt_prev_state with
    | None -> total
    | Some _ when not is_new_pos -> total
    | Some prev_state ->
      let { row = blocked_row; col = blocked_col; _ } = curr_state in
      total + Bool.to_int (blocking_creates_cycle grid blocked_row blocked_col prev_state))
;;

let grid = read () in
let start_row, start_col = find_start grid in
let start_state = { row = start_row; col = start_col; dir_id = start_dir_id } in
print_endline (string_of_int (solve_part1 grid start_state));
print_endline (string_of_int (solve_part2 grid start_state))
