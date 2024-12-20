open Core

let start_char = 'S'
let end_char = 'E'
let wall_char = '#'
let dirs = [ 0, 1; 1, 0; 0, -1; -1, 0 ]
let inf = 100000000
let part1_max_cheat_dist = 2
let part2_max_cheat_dist = 20
let part1_min_dist_save = 100 (* Set to 1 for sample input *)
let part2_min_dist_save = 100 (* Set to 50 for sample input *)

type tile =
  | Wall
  | Track

let char_to_tile chr = if Char.equal chr wall_char then Wall else Track

let findi_char_exn target_chr =
  List.find_mapi_exn ~f:(fun r row ->
    String.find_mapi row ~f:(fun c chr ->
      Option.some_if (Char.equal chr target_chr) (r, c)))
;;

let read () =
  let raw_grid = In_channel.(input_lines stdin) in
  let start_pos = findi_char_exn start_char raw_grid in
  let end_pos = findi_char_exn end_char raw_grid in
  let grid =
    Array.of_list_map raw_grid ~f:(fun row ->
      String.to_array row |> Array.map ~f:char_to_tile)
  in
  grid, start_pos, end_pos
;;

let is_same_pos (r1, c1) (r2, c2) = r1 = r2 && c1 = c2
let dist_between (r1, c1) (r2, c2) = abs (r2 - r1) + abs (c2 - c1)
let get_neighbours (r, c) = List.map dirs ~f:(fun (dr, dc) -> r + dr, c + dc)

let get_tracks_in_radius grid (r, c) radius =
  let height = Array.length grid in
  let width = Array.length grid.(0) in
  Sequence.range (max (r - radius) 0) (min (r + radius + 1) height)
  |> Sequence.concat_map ~f:(fun r2 ->
    let d = radius - abs (r - r2) in
    let col_nums = Sequence.range (max (c - d) 0) (min (c + d + 1) width) in
    Sequence.filter_map col_nums ~f:(fun c2 ->
      match grid.(r2).(c2) with
      | Wall -> None
      | Track -> Some (r2, c2)))
;;

let find_dists grid start_pos end_pos =
  let height = Array.length grid in
  let width = Array.length grid.(0) in
  let dists = Array.make_matrix ~dimx:height ~dimy:width inf in
  (* Problem statement states that only a single path going from start to end exists *)
  let rec dfs curr_pos prev_pos step =
    dists.(fst curr_pos).(snd curr_pos) <- step;
    if not (is_same_pos curr_pos end_pos)
    then (
      let next_pos =
        List.find_exn (get_neighbours curr_pos) ~f:(fun ((r2, c2) as pos) ->
          match grid.(r2).(c2) with
          | Wall -> false
          | Track -> not (is_same_pos pos prev_pos))
      in
      dfs next_pos curr_pos (step + 1))
  in
  dfs start_pos (-1, -1) 0;
  dists
;;

let count_useful_cheats ~max_cheat_dist ~min_dist_save grid start_pos end_pos =
  let dists = find_dists grid start_pos end_pos in
  let is_useful_cheat (r, c) (r2, c2) =
    let dist_saved = dists.(r2).(c2) - dists.(r).(c) - dist_between (r, c) (r2, c2) in
    dist_saved >= min_dist_save
  in
  Array.foldi grid ~init:0 ~f:(fun r total row ->
    Array.foldi row ~init:total ~f:(fun c total cell ->
      match cell with
      | Wall -> total
      | Track ->
        let reachable_tracks = get_tracks_in_radius grid (r, c) max_cheat_dist in
        total + Sequence.count reachable_tracks ~f:(is_useful_cheat (r, c))))
;;

let solve_part1 =
  count_useful_cheats
    ~max_cheat_dist:part1_max_cheat_dist
    ~min_dist_save:part1_min_dist_save
;;

let solve_part2 =
  count_useful_cheats
    ~max_cheat_dist:part2_max_cheat_dist
    ~min_dist_save:part2_min_dist_save
;;

let () =
  let grid, start_pos, end_pos = read () in
  let part1_ans = solve_part1 grid start_pos end_pos in
  let part2_ans = solve_part2 grid start_pos end_pos in
  printf "%d\n%d\n" part1_ans part2_ans
;;
