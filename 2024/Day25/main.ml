open Core

let max_height = 7

let parse_schematic raw_schematic =
  let schematic =
    String.split_lines raw_schematic
    |> Array.of_list_map ~f:String.to_array
    |> Array.transpose_exn
  in
  let is_lock = Char.equal schematic.(0).(0) '#' in
  let heights = Array.map schematic ~f:(Array.count ~f:(Char.equal '#')) in
  if is_lock then First heights else Second heights
;;

let read () =
  In_channel.(input_all stdin)
  |> Re.split (Re.compile (Re.str "\n\n"))
  |> List.partition_map ~f:parse_schematic
;;

let can_unlock lock key =
  Array.for_all2_exn lock key ~f:(fun lock_pin_height key_bit_height ->
    lock_pin_height + key_bit_height <= max_height)
;;

let solve lock_list key_list =
  List.sum (module Int) lock_list ~f:(fun lock ->
    List.count key_list ~f:(can_unlock lock))
;;

let () =
  let lock_list, key_list = read () in
  let ans = solve lock_list key_list in
  printf "%d\n" ans
;;
