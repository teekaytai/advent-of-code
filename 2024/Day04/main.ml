open Core

let in_bounds h w r c = 0 <= r && r < h && 0 <= c && c < w

let matches_xmas_line grid r c dr dc =
  let h = Array.length grid in
  let w = Array.length grid.(0) in
  Array.for_alli [| 'X'; 'M'; 'A'; 'S' |] ~f:(fun i letter ->
    let r2 = r + (i * dr) in
    let c2 = c + (i * dc) in
    in_bounds h w r2 c2 && Char.equal grid.(r2).(c2) letter)
;;

let is_ms_pair letter1 letter2 =
  (Char.equal letter1 'M' && Char.equal letter2 'S')
  || (Char.equal letter1 'S' && Char.equal letter2 'M')
;;

let matches_xmas_cross grid r c =
  let h = Array.length grid in
  let w = Array.length grid.(0) in
  if r >= h - 2 || c >= w - 2 || not (Char.equal grid.(r + 1).(c + 1) 'A')
  then false
  else (
    let tl_letter = grid.(r).(c) in
    let tr_letter = grid.(r).(c + 2) in
    let bl_letter = grid.(r + 2).(c) in
    let br_letter = grid.(r + 2).(c + 2) in
    is_ms_pair tl_letter br_letter && is_ms_pair tr_letter bl_letter)
;;

let solve_part1 grid =
  let dirs = [| -1, -1; -1, 0; -1, 1; 0, -1; 0, 1; 1, -1; 1, 0; 1, 1 |] in
  Array.foldi grid ~init:0 ~f:(fun r total row ->
    total
    + Array.foldi row ~init:0 ~f:(fun c subtotal _ ->
      subtotal + Array.count dirs ~f:(fun (dr, dc) -> matches_xmas_line grid r c dr dc)))
;;

let solve_part2 grid =
  Array.foldi grid ~init:0 ~f:(fun r total row ->
    total + Array.counti row ~f:(fun c _ -> matches_xmas_cross grid r c))
;;

let grid = Array.of_list_map ~f:String.to_array In_channel.(input_lines stdin) in
print_endline (string_of_int (solve_part1 grid));
print_endline (string_of_int (solve_part2 grid))
