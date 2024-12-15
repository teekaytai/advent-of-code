open Core

let start_char = '@'

type cell_t =
  | Wall
  | Empty
  | Box
  | Box_left
  | Box_right

type move_t =
  | Up
  | Right
  | Down
  | Left

type state =
  { grid : cell_t array array
  ; r : int ref
  ; c : int ref
  }

let char_to_cell = function
  | '#' -> Wall
  | 'O' -> Box
  | '.' | '@' -> Empty
  | _ -> invalid_arg "Unknown cell character"
;;

let char_to_move = function
  | '^' -> Up
  | '>' -> Right
  | 'v' -> Down
  | '<' -> Left
  | _ -> invalid_arg "Unknown move character"
;;

let pos_equal = Tuple2.equal ~eq1:Int.( = ) ~eq2:Int.( = )

let move_pos move (r, c) =
  match move with
  | Up -> r - 1, c
  | Right -> r, c + 1
  | Down -> r + 1, c
  | Left -> r, c - 1
;;

let parse_grid raw_grid =
  let start_r, start_c =
    List.find_mapi_exn raw_grid ~f:(fun r row ->
      String.find_mapi row ~f:(fun c chr ->
        Option.some_if (Char.equal chr start_char) (r, c)))
  in
  let grid =
    Array.of_list_map raw_grid ~f:(fun row ->
      String.to_array row |> Array.map ~f:char_to_cell)
  in
  grid, start_r, start_c
;;

let parse_moves =
  List.concat_map ~f:(fun line -> List.map (String.to_list line) ~f:char_to_move)
;;

let expand_grid =
  Array.map
    ~f:
      (Array.concat_map ~f:(function
        | Wall -> [| Wall; Wall |]
        | Box -> [| Box_left; Box_right |]
        | Empty -> [| Empty; Empty |]
        | Box_left | Box_right -> invalid_arg "No big boxes should be in original grid"))
;;

let box_gps_sum =
  Array.foldi ~init:0 ~f:(fun r total row ->
    Array.foldi row ~init:total ~f:(fun c total cell ->
      match cell with
      | Box | Box_left -> total + (100 * r) + c
      | Wall | Empty | Box_right -> total))
;;

(* Find correct order to push boxes using topological sort done with post-order dfs.
   The boxes further from the robot should be moved first to make way for the closer ones.
   If any box hits a wall, returns None *)
let find_push_order state move =
  let grid = state.grid in
  let start_pos = !(state.r), !(state.c) in
  let rec dfs curr_pos pos_order =
    if List.mem pos_order curr_pos ~equal:pos_equal
    then Some pos_order
    else (
      let ((new_r, new_c) as new_pos) = move_pos move curr_pos in
      let opt_new_pos_order =
        match grid.(new_r).(new_c), move with
        | Wall, _ -> None
        | Empty, _ -> Some pos_order
        | Box, _ | Box_left, Left | Box_left, Right | Box_right, Left | Box_right, Right
          -> dfs new_pos pos_order
        | Box_left, Up | Box_left, Down ->
          dfs new_pos pos_order |> Option.find_map ~f:(dfs (new_r, new_c + 1))
        | Box_right, Up | Box_right, Down ->
          dfs new_pos pos_order |> Option.find_map ~f:(dfs (new_r, new_c - 1))
      in
      Option.map opt_new_pos_order ~f:(List.cons curr_pos))
  in
  Option.map (dfs start_pos []) ~f:List.rev
;;

let make_pushes grid move push_order =
  List.iter push_order ~f:(fun ((curr_r, curr_c) as pos) ->
    let next_r, next_c = move_pos move pos in
    grid.(next_r).(next_c) <- grid.(curr_r).(curr_c);
    grid.(curr_r).(curr_c) <- Empty)
;;

let update_state state move =
  find_push_order state move
  |> Option.iter ~f:(fun push_order ->
    make_pushes state.grid move push_order;
    let new_r, new_c = move_pos move (!(state.r), !(state.c)) in
    state.r := new_r;
    state.c := new_c)
;;

let read () =
  let lines = In_channel.(input_lines stdin) in
  let sep_idx = List.findi_exn lines ~f:(fun _ line -> String.is_empty line) |> fst in
  let grid, start_r, start_c = parse_grid (List.take lines sep_idx) in
  let moves = parse_moves (List.drop lines (sep_idx + 1)) in
  grid, moves, start_r, start_c
;;

let solve_part1 original_grid moves ~start_r ~start_c =
  let state =
    { grid = Array.copy_matrix original_grid; r = ref start_r; c = ref start_c }
  in
  List.iter moves ~f:(update_state state);
  box_gps_sum state.grid
;;

let solve_part2 original_grid moves ~start_r ~start_c =
  let grid = expand_grid original_grid in
  let new_start_c = start_c * 2 in
  let state = { grid; r = ref start_r; c = ref new_start_c } in
  List.iter moves ~f:(update_state state);
  box_gps_sum state.grid
;;

let () =
  let grid, moves, start_r, start_c = read () in
  let part1_ans = solve_part1 grid moves ~start_r ~start_c in
  let part2_ans = solve_part2 grid moves ~start_r ~start_c in
  printf "%d\n%d\n" part1_ans part2_ans
;;
