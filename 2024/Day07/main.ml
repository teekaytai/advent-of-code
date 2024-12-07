open Core

let concat_ints num1 num2 = Int.of_string (Printf.sprintf "%d%d" num1 num2)

let read () =
  List.map
    In_channel.(input_lines stdin)
    ~f:(fun line ->
      line
      |> String.filter ~f:(fun chr -> not (Char.equal chr ':'))
      |> String.split ~on:' '
      |> List.map ~f:Int.of_string
      |> function
      | target :: operands -> target, operands
      | _ -> invalid_arg "line should have a target value")
;;

let rec is_satisfiable ~ops target operands =
  match operands with
  | [] -> invalid_arg "operands list should not be empty"
  | [ num ] -> num = target
  | num1 :: num2 :: tail ->
    List.exists ops ~f:(fun op -> is_satisfiable ~ops target (op num1 num2 :: tail))
;;

let sum_possible_targets ~ops =
  List.fold ~init:0 ~f:(fun total (target, operands) ->
    if is_satisfiable ~ops target operands then total + target else total)
;;

let solve_part1 = sum_possible_targets ~ops:[ Int.( + ); Int.( * ) ]
let solve_part2 = sum_possible_targets ~ops:[ Int.( + ); Int.( * ); concat_ints ];;

let incomplete_equations = read () in
print_endline (Int.to_string (solve_part1 incomplete_equations));
print_endline (Int.to_string (solve_part2 incomplete_equations))
