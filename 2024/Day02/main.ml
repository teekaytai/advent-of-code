open Core

let read () =
  let string_to_int_list =
    Fn.compose (List.map ~f:int_of_string) (String.split ~on:' ')
  in
  List.map ~f:string_to_int_list In_channel.(input_lines stdin)
;;

let is_safe level_list =
  let min_diff = 1 in
  let max_diff = 3 in
  let trunc_level_list = List.drop_last_exn level_list in
  let level_list_tail = List.tl_exn level_list in
  let differences = List.map2_exn ~f:( - ) trunc_level_list level_list_tail in
  List.for_all ~f:(fun x -> min_diff <= x && x <= max_diff) differences
  || List.for_all ~f:(fun x -> -max_diff <= x && x <= -min_diff) differences
;;

let solve_part1 = List.count ~f:is_safe

let solve_part2 =
  let dropi lst dropped_idx = List.filteri ~f:(fun i _ -> i <> dropped_idx) lst in
  List.count ~f:(fun level_list ->
    List.existsi level_list ~f:(fun dropped_idx _ ->
      is_safe (dropi level_list dropped_idx)))
;;

let level_lists = read () in
print_endline (string_of_int (solve_part1 level_lists));
print_endline (string_of_int (solve_part2 level_lists))
