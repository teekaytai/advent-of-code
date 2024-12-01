open Core

let rec read list_a list_b =
  try
    let num_pair =
      In_channel.(input_line_exn stdin)
      |> Str.split (Str.regexp " +")
      |> List.map ~f:int_of_string
    in
    let num_a, num_b =
      match num_pair with
      | [ a; b ] -> a, b
      | _ -> failwith "Input line should have exactly two integers"
    in
    read (num_a :: list_a) (num_b :: list_b)
  with
  | End_of_file -> List.rev list_a, List.rev list_b
;;

let solve_part1 list_a list_b =
  let sorted_list_a = List.sort ~compare list_a in
  let sorted_list_b = List.sort ~compare list_b in
  List.fold2_exn sorted_list_a sorted_list_b ~init:0 ~f:(fun total num_a num_b ->
    total + abs (num_a - num_b))
;;

let solve_part2 list_a list_b =
  let b_counter =
    List.fold
      list_b
      ~init:(Hashtbl.create (module Int))
      ~f:(fun counter num ->
        Hashtbl.update counter num ~f:(fun count -> Option.value count ~default:0 + 1);
        counter)
  in
  List.fold list_a ~init:0 ~f:(fun total num ->
    total + (num * Option.value (Hashtbl.find b_counter num) ~default:0))
;;

let list_a, list_b = read [] [] in
print_endline (string_of_int (solve_part1 list_a list_b));
print_endline (string_of_int (solve_part2 list_a list_b))
