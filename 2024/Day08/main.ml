open Core

let empty_space = '.'
let rec gcd x y = if x = 0 then y else gcd (y % x) x
let is_in_bounds height width (r, c) = 0 <= r && r < height && 0 <= c && c < width

let iter_all_pairs lst ~f =
  let rec loop lst =
    match lst with
    | [] -> ()
    | head :: tail ->
      List.iter tail ~f:(f head);
      loop tail
  in
  loop lst
;;

let generate_points_in_line ~height ~width start_point ~dr ~dc =
  Sequence.unfold ~init:start_point ~f:(fun ((r, c) as curr) ->
    if is_in_bounds height width curr then Some (curr, (r + dr, c + dc)) else None)
  |> Sequence.to_list
;;

let get_antenna_locations grid =
  let freq_to_antenna_locs = Hashtbl.create (module Char) in
  List.iteri grid ~f:(fun r row ->
    String.iteri row ~f:(fun c cell ->
      if not (Char.equal cell empty_space)
      then
        Hashtbl.update freq_to_antenna_locs cell ~f:(function
          | None -> [ r, c ]
          | Some antenna_locs -> (r, c) :: antenna_locs)));
  freq_to_antenna_locs
;;

let count_antinodes height width find_antinodes freq_to_antenna_locs =
  let has_antinodes = Array.make_matrix ~dimx:height ~dimy:width false in
  Hashtbl.iter freq_to_antenna_locs ~f:(fun antenna_locs ->
    iter_all_pairs antenna_locs ~f:(fun antenna1 antenna2 ->
      List.iter (find_antinodes antenna1 antenna2) ~f:(fun antinode ->
        has_antinodes.(fst antinode).(snd antinode) <- true)));
  Array.fold has_antinodes ~init:0 ~f:(fun total row -> total + Array.count ~f:Fn.id row)
;;

let solve_part1 height width =
  count_antinodes height width (fun (r1, c1) (r2, c2) ->
    List.filter
      ~f:(is_in_bounds height width)
      [ (r1 * 2) - r2, (c1 * 2) - c2; (r2 * 2) - r1, (c2 * 2) - c1 ])
;;

let solve_part2 height width =
  count_antinodes height width (fun (r1, c1) (r2, c2) ->
    let r_diff = r2 - r1 in
    let c_diff = c2 - c1 in
    let g = gcd (Int.abs r_diff) (Int.abs c_diff) in
    let dr = r_diff / g in
    let dc = c_diff / g in
    let points1 =
      generate_points_in_line ~height ~width (r1 - dr, c1 - dc) ~dr:(-dr) ~dc:(-dc)
    in
    let points2 = generate_points_in_line ~height ~width (r1, c1) ~dr ~dc in
    List.rev_append points1 points2)
;;

let () =
  let grid = In_channel.(input_lines stdin) in
  let height = List.length grid in
  let width = String.length (List.hd_exn grid) in
  let freq_to_antenna_locs = get_antenna_locations grid in
  let part1_ans = solve_part1 height width freq_to_antenna_locs in
  let part2_ans = solve_part2 height width freq_to_antenna_locs in
  printf "%d\n%d\n" part1_ans part2_ans
;;
