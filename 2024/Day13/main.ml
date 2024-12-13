open Core

let read () =
  let re_nums = Re.compile (Re.rep1 Re.digit) in
  Re.all re_nums In_channel.(input_all stdin)
  |> List.map ~f:(fun _match -> Int.of_string (Re.Group.get _match 0))
  |> List.chunks_of ~length:6
;;

(* Solves the system of equations Ax = b, i.e. a11 * x1 + a12 * x2 = b1, a21 * x1 + a22 * x2 = b2 *)
(* Returns None if system is not full rank or if either x1 or x2 is not an integer *)
let solve_simul ~a11 ~a12 ~a21 ~a22 ~b1 ~b2 =
  if (a11 * a22) - (a12 * a21) = 0
  then None
  else (
    let p = (a22 * b1) - (a12 * b2) in
    let q = (a11 * a22) - (a12 * a21) in
    if p mod q <> 0
    then None
    else (
      let x1 = p / q in
      let r = b1 - (a11 * x1) in
      if r mod a12 <> 0
      then None
      else (
        let x2 = r / a12 in
        Some (x1, x2))))
;;

let total_tokens_needed ?(offset = 0) =
  List.sum
    (module Int)
    ~f:(function
      | [ a11; a21; a12; a22; b1; b2 ] ->
        (match solve_simul ~a11 ~a12 ~a21 ~a22 ~b1:(b1 + offset) ~b2:(b2 + offset) with
         | None -> 0
         | Some (x1, x2) -> (3 * x1) + x2)
      | _ -> invalid_arg "Each machine should be defined with exactly 6 integers")
;;

let solve_part1 = total_tokens_needed
let solve_part2 = total_tokens_needed ~offset:10000000000000

let () =
  let machines = read () in
  let part1_ans = solve_part1 machines in
  let part2_ans = solve_part2 machines in
  printf "%d\n%d\n" part1_ans part2_ans
;;
