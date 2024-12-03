open Core

let mul_pattern = {|mul\((\d+),(\d+)\)|}
let do_pattern = {|do\(\)|}
let dont_pattern = {|don't\(\)|}
let all_instr_patterns = String.concat ~sep:"|" [ mul_pattern; do_pattern; dont_pattern ]
let re_mul = Re.Perl.compile_pat mul_pattern
let re_all = Re.Perl.compile_pat all_instr_patterns

let get_mul_result mul_instruction =
  let num1 = int_of_string (Re.Group.get mul_instruction 1) in
  let num2 = int_of_string (Re.Group.get mul_instruction 2) in
  num1 * num2
;;

let solve_part1 memory =
  let matches = Re.all re_mul memory in
  List.fold matches ~init:0 ~f:(fun total instruction ->
    total + get_mul_result instruction)
;;

let solve_part2 memory =
  let matches = Re.all re_all memory in
  List.fold matches ~init:(0, true) ~f:(fun (total, is_enabled) instruction ->
    match Re.Group.get instruction 0 with
    | "do()" -> total, true
    | "don't()" -> total, false
    | _ when is_enabled -> total + get_mul_result instruction, is_enabled
    | _ -> total, is_enabled)
  |> fst
;;

let full_input = In_channel.(input_all stdin) in
print_endline (string_of_int (solve_part1 full_input));
print_endline (string_of_int (solve_part2 full_input))
