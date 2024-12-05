open Core

let parse_rules =
  List.fold
    ~init:(Hashtbl.create (module Int))
    ~f:(fun rules line ->
      let earlier_page, later_page =
        match List.map ~f:int_of_string (String.split ~on:'|' line) with
        | [ x; y ] -> x, y
        | _ -> invalid_arg "Rules should consist of exactly two integers"
      in
      Hashtbl.update rules earlier_page ~f:(fun later_pages_option ->
        let later_pages =
          Option.value later_pages_option ~default:(Hash_set.create (module Int))
        in
        Hash_set.add later_pages later_page;
        later_pages);
      rules)
;;

let parse_updates =
  List.map ~f:(Fn.compose (Array.of_list_map ~f:int_of_string) (String.split ~on:','))
;;

let read () =
  let lines = In_channel.(input_lines stdin) in
  let sep_idx = fst (List.findi_exn ~f:(fun _ line -> String.is_empty line) lines) in
  let ordering_rules = parse_rules (List.take lines sep_idx) in
  let update_orders = parse_updates (List.drop lines (sep_idx + 1)) in
  ordering_rules, update_orders
;;

let is_earlier_page ordering_rules curr_page next_page =
  match Hashtbl.find ordering_rules curr_page with
  | Some later_pages -> Hash_set.mem later_pages next_page
  | None -> false
;;

let compare_pages ordering_rules page1 page2 =
  if is_earlier_page ordering_rules page1 page2
  then -1
  else if is_earlier_page ordering_rules page2 page1
  then 1
  else 0
;;

let get_middle_elt arr = arr.(Array.length arr / 2)

let solve (ordering_rules, update_orders) =
  let compare = compare_pages ordering_rules in
  List.fold update_orders ~init:(0, 0) ~f:(fun (total1, total2) update_order ->
    if Array.is_sorted ~compare update_order
    then total1 + get_middle_elt update_order, total2
    else (
      Array.sort ~compare update_order;
      total1, total2 + get_middle_elt update_order))
;;

let part1_ans, part2_ans = solve (read ()) in
print_endline (string_of_int part1_ans);
print_endline (string_of_int part2_ans)
