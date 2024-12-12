open Core

let dirs = [| -1, 0; 0, 1; 1, 0; 0, -1 |]
let rotate_dir (dr, dc) = dc, -dr

let is_in_region grid r c plant =
  r >= 0
  && r < Array.length grid
  && c >= 0
  && c < Array.length grid.(0)
  && Char.equal grid.(r).(c) plant
;;

(* Check if the cell next to this one has an edge facing the same way. *)
(* If it does not, then we know the current edge is the last one in this side of the region. *)
let is_last_edge_in_side grid ~r ~c ~dr ~dc =
  let plant = grid.(r).(c) in
  let dir_to_adj_cell = rotate_dir (dr, dc) in
  let adj_r = r + fst dir_to_adj_cell in
  let adj_c = c + snd dir_to_adj_cell in
  let diag_r = adj_r + dr in
  let diag_c = adj_c + dc in
  let adj_cell_has_aligned_edge =
    is_in_region grid adj_r adj_c plant && not (is_in_region grid diag_r diag_c plant)
  in
  not adj_cell_has_aligned_edge
;;

let read () = In_channel.(input_lines stdin) |> Array.of_list_map ~f:String.to_array

let measure_region grid visited ~start_r ~start_c ~should_count_edge =
  visited.(start_r).(start_c) <- true;
  let plant = grid.(start_r).(start_c) in
  let rec dfs r c =
    Array.fold dirs ~init:(1, 0) ~f:(fun (area, perimeter) (dr, dc) ->
      let r2 = r + dr in
      let c2 = c + dc in
      match is_in_region grid r2 c2 plant with
      | true when visited.(r2).(c2) -> area, perimeter
      | true ->
        visited.(r2).(c2) <- true;
        let a, p = dfs r2 c2 in
        area + a, perimeter + p
      | false -> area, perimeter + Bool.to_int (should_count_edge ~r ~c ~dr ~dc))
  in
  dfs start_r start_c
;;

let fold_regions grid ~init ~process_region =
  let height = Array.length grid in
  let width = Array.length grid.(0) in
  let visited = Array.make_matrix ~dimx:height ~dimy:width false in
  Array.foldi grid ~init ~f:(fun r acc row ->
    Array.foldi row ~init:acc ~f:(fun c sub_acc _ ->
      if visited.(r).(c) then sub_acc else process_region sub_acc visited ~r ~c))
;;

let find_fence_cost grid ~should_count_edge =
  fold_regions grid ~init:0 ~process_region:(fun total visited ~r ~c ->
    let area, perimeter =
      measure_region grid visited ~start_r:r ~start_c:c ~should_count_edge
    in
    total + (area * perimeter))
;;

let solve_part1 grid =
  let should_count_edge ~r:_ ~c:_ ~dr:_ ~dc:_ = true in
  find_fence_cost grid ~should_count_edge
;;

let solve_part2 grid =
  (* Count one edge per side to effectively count the number of sides of region *)
  let should_count_edge = is_last_edge_in_side grid in
  find_fence_cost grid ~should_count_edge
;;

let () =
  let grid = read () in
  let part1_ans = solve_part1 grid in
  let part2_ans = solve_part2 grid in
  printf "%d\n%d\n" part1_ans part2_ans
;;
