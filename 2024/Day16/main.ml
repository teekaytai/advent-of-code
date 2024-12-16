open Core

let start_char = 'S'
let end_char = 'E'
let wall_char = '#'
let dirs = [| 0, 1; 1, 0; 0, -1; -1, 0 |]
let start_dir_id = 0
let num_dirs = 4
let turn_cost = 1000

type tile =
  | Empty
  | Blocked

module Cell = struct
  module T = struct
    type t =
      { row : int
      ; col : int
      }
    [@@deriving compare, sexp_of]

    let create row col = { row; col }
  end

  include T
  include Comparator.Make (T)
end

module State = struct
  type t =
    { row : int
    ; col : int
    ; dir_id : int
    }
  [@@deriving compare, sexp_of, hash]

  let create row col dir_id = { row; col; dir_id }
end

module Pq_node = struct
  module T = struct
    type t =
      { score : int
      ; state : State.t
      }
    [@@deriving compare, sexp_of]

    let create score state = { score; state }
  end

  include T
  include Comparator.Make (T)
end

type state_paths_info =
  { min_score : int
  ; paths_cells : (Cell.t, Cell.comparator_witness) Set.t
  }

let findi_char_exn target_chr =
  List.find_mapi_exn ~f:(fun r row ->
    String.find_mapi row ~f:(fun c chr ->
      Option.some_if (Char.equal chr target_chr) (Cell.create r c)))
;;

let read () =
  let lines = In_channel.(input_lines stdin) in
  let start_cell = findi_char_exn start_char lines in
  let end_cell = findi_char_exn end_char lines in
  let grid =
    Array.of_list_map lines ~f:(fun row ->
      String.to_array row
      |> Array.map ~f:(fun chr -> if Char.equal chr wall_char then Blocked else Empty))
  in
  grid, start_cell, end_cell
;;

let init_dijkstra ({ row = start_row; col = start_col } as start_cell : Cell.t) =
  let start_state = State.create start_row start_col start_dir_id in
  let start_state_paths_info =
    { min_score = 0; paths_cells = Set.singleton (module Cell) start_cell }
  in
  (* For each state reached, store the minimum score it has been reached with so far,
     and the Set of Cells on any best path to that state. *)
  let state_to_paths_info = Hashtbl.create (module State) in
  Hashtbl.add_exn state_to_paths_info ~key:start_state ~data:start_state_paths_info;
  let pq = Pairing_heap.create ~cmp:Pq_node.compare () in
  Pairing_heap.add pq (Pq_node.create 0 start_state);
  state_to_paths_info, pq
;;

let get_next_states ({ row; col; _ } : State.t) =
  Array.mapi dirs ~f:(fun next_dir_id (dr, dc) ->
    let next_row = row + dr in
    let next_col = col + dc in
    State.create next_row next_col next_dir_id)
;;

let is_end_state ({ row; col; _ } : State.t) (end_cell : Cell.t) =
  row = end_cell.row && col = end_cell.col
;;

let calc_next_score score (curr_state : State.t) (next_state : State.t) =
  let curr_dir_id = curr_state.dir_id in
  let next_dir_id = next_state.dir_id in
  let turn_amount =
    min ((curr_dir_id - next_dir_id) % num_dirs) ((next_dir_id - curr_dir_id) % num_dirs)
  in
  score + 1 + (turn_cost * turn_amount)
;;

let process_pq_node grid state_to_paths_info pq pq_node curr_paths_cells =
  let ({ score = curr_score; state = curr_state } : Pq_node.t) = pq_node in
  let next_states = get_next_states curr_state in
  Array.iter next_states ~f:(fun next_state ->
    let ({ row = next_row; col = next_col; _ } : State.t) = next_state in
    let next_score = calc_next_score curr_score curr_state next_state in
    let opt_next_state_paths_info = Hashtbl.find state_to_paths_info next_state in
    match grid.(next_row).(next_col), opt_next_state_paths_info with
    | Blocked, _ -> ()
    | Empty, Some { min_score; _ } when next_score > min_score -> ()
    | Empty, Some { min_score; paths_cells = next_paths_cells }
      when next_score = min_score ->
      (* Found another equally good path to this next state, update Set of Cells found on best paths *)
      let updated_paths_info =
        { min_score; paths_cells = Set.union curr_paths_cells next_paths_cells }
      in
      Hashtbl.set state_to_paths_info ~key:next_state ~data:updated_paths_info
    | Empty, _ ->
      (* Found lowest score path to this next state, (re-)set path info of the state *)
      let next_cell = Cell.create next_row next_col in
      let next_paths_info =
        { min_score = next_score; paths_cells = Set.add curr_paths_cells next_cell }
      in
      Hashtbl.set state_to_paths_info ~key:next_state ~data:next_paths_info;
      let next_pq_node : Pq_node.t = { score = next_score; state = next_state } in
      Pairing_heap.add pq next_pq_node)
;;

let solve grid start_cell end_cell =
  let state_to_paths_info, pq = init_dijkstra start_cell in
  let end_state_reached = ref None in
  while Option.is_none !end_state_reached do
    let ({ score; state } as pq_node : Pq_node.t) = Pairing_heap.pop_exn pq in
    let { min_score; paths_cells } = Hashtbl.find_exn state_to_paths_info state in
    (* Consider this pq node only if it reflects the lowest scoring path found to this state *)
    if score = min_score
    then
      if is_end_state state end_cell
      then end_state_reached := Some state
      else process_pq_node grid state_to_paths_info pq pq_node paths_cells
  done;
  let { min_score = end_min_score; paths_cells = end_paths_cells } =
    Hashtbl.find_exn state_to_paths_info (Option.value_exn !end_state_reached)
  in
  end_min_score, Set.length end_paths_cells
;;

let () =
  let grid, start_cell, end_cell = read () in
  let part1_ans, part2_ans = solve grid start_cell end_cell in
  printf "%d\n%d\n" part1_ans part2_ans
;;
