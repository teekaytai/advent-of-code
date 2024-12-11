open Core

module IntPair = struct
  type t = int * int [@@deriving compare, sexp_of, hash]
end

let read () =
  In_channel.(input_line_exn stdin) |> String.split ~on:' ' |> List.map ~f:Int.of_string
;;

let memoize m f =
  let memo = Hashtbl.create m in
  fun x -> Hashtbl.find_or_add memo x ~default:(fun () -> f x)
;;

let memoize_rec m nonrec_f =
  let fref = ref (fun _ -> assert false) in
  let memo_f = memoize m (fun x -> nonrec_f !fref x) in
  fref := memo_f;
  memo_f
;;

let count_stones rec_count_stones (blinks, stone) =
  if blinks = 0
  then 1
  else if stone = 0
  then rec_count_stones (blinks - 1, 1)
  else (
    let num_digits = Int.of_float (Float.log10 (Int.to_float stone)) + 1 in
    if num_digits % 2 = 0
    then (
      let mid_pow_10 = Int.pow 10 (num_digits / 2) in
      let fst_half_stone = stone / mid_pow_10 in
      let snd_half_stone = stone % mid_pow_10 in
      rec_count_stones (blinks - 1, fst_half_stone)
      + rec_count_stones (blinks - 1, snd_half_stone))
    else rec_count_stones (blinks - 1, stone * 2024))
;;

let memo_count_stones = memoize_rec (module IntPair) count_stones

let solve_part1 =
  List.fold ~init:0 ~f:(fun total stone -> total + memo_count_stones (25, stone))
;;

let solve_part2 =
  List.fold ~init:0 ~f:(fun total stone -> total + memo_count_stones (75, stone))
;;

let () =
  let stones = read () in
  let part1_ans = solve_part1 stones in
  let part2_ans = solve_part2 stones in
  printf "%d\n%d\n" part1_ans part2_ans
;;
