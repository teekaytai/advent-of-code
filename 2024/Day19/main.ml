open Core

module String_int_pair = struct
  type t = string * int [@@deriving compare, sexp_of, hash]
end

let read () =
  let towels =
    In_channel.(input_line_exn stdin)
    |> Re.split (Re.compile (Re.str ", "))
    |> Hash_set.of_list (module String)
  in
  assert (String.is_empty In_channel.(input_line_exn stdin));
  let designs = In_channel.(input_lines stdin) in
  towels, designs
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

let make_partitions_counter towels ~zero ~one ~add =
  let count_partitions rec_count_partitions (design, lo) =
    let n = String.length design in
    if lo = n
    then one
    else
      Sequence.fold (Sequence.range lo n) ~init:zero ~f:(fun acc hi ->
        if Hash_set.mem towels (String.slice design lo (hi + 1))
        then add acc (rec_count_partitions (design, hi + 1))
        else acc)
  in
  let helper = memoize_rec (module String_int_pair) count_partitions in
  fun design -> helper (design, 0)
;;

let solve_part1 towels =
  let can_partition = make_partitions_counter towels ~zero:false ~one:true ~add:( || ) in
  List.count ~f:can_partition
;;

let solve_part2 towels =
  let count_partitions = make_partitions_counter towels ~zero:0 ~one:1 ~add:( + ) in
  List.sum (module Int) ~f:count_partitions
;;

let () =
  let towels, designs = read () in
  let part1_ans = solve_part1 towels designs in
  let part2_ans = solve_part2 towels designs in
  printf "%d\n%d\n" part1_ans part2_ans
;;
