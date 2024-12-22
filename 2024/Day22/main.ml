open Core

let max_generations = 2000
let price_changes_seq_len = 4
let min_price_change = -10
let max_price_change = 10
let price_change_range = max_price_change - min_price_change + 1
let rolling_hash_mod = Int.pow price_change_range (price_changes_seq_len - 1)
let read () = In_channel.(input_lines stdin) |> List.map ~f:Int.of_string
let mix_and_prune num1 num2 = num1 lxor num2 % 16777216

let gen_next_secret_num secret_num =
  let t1 = mix_and_prune secret_num (secret_num * 64) in
  let t2 = mix_and_prune t1 (t1 / 32) in
  mix_and_prune t2 (t2 * 2048)
;;

let get_price secret_num = secret_num % 10

(* Since all price changes will always be between -10 and 10, they can be compressed into
   a single hash value for faster hashing and to reduce memory consumption. A rolling hash is
   used to further speed up computing new hashes. *)
let update_prices_rolling_hash price_changes_hash price_change =
  (price_changes_hash % rolling_hash_mod * price_change_range)
  + (price_change - min_price_change)
;;

let find_possible_banana_buys secret_num =
  let price_changes_to_bananas = Hashtbl.create (module Int) in
  let rec loop step price_changes_hash curr_secret =
    if step >= price_changes_seq_len
    then
      if not (Hashtbl.mem price_changes_to_bananas price_changes_hash)
      then
        Hashtbl.add_exn
          price_changes_to_bananas
          ~key:price_changes_hash
          ~data:(get_price curr_secret);
    if step < max_generations
    then (
      let next_secret = gen_next_secret_num curr_secret in
      let new_price_change = get_price next_secret - get_price curr_secret in
      let new_price_changes_hash =
        update_prices_rolling_hash price_changes_hash new_price_change
      in
      loop (step + 1) new_price_changes_hash next_secret)
  in
  loop 0 0 secret_num;
  price_changes_to_bananas
;;

let solve_part1 =
  List.sum (module Int) ~f:(Fn.apply_n_times ~n:max_generations gen_next_secret_num)
;;

let solve_part2 secret_nums =
  let price_changes_to_banana_totals = Hashtbl.create (module Int) in
  List.iter secret_nums ~f:(fun secret_num ->
    let price_changes_to_bananas = find_possible_banana_buys secret_num in
    Hashtbl.merge_into
      ~src:price_changes_to_bananas
      ~dst:price_changes_to_banana_totals
      ~f:(fun ~key:_ bananas_bought opt_banana_total ->
        let new_banana_count =
          Option.value_map
            opt_banana_total
            ~default:bananas_bought
            ~f:(Int.( + ) bananas_bought)
        in
        Set_to new_banana_count));
  List.max_elt ~compare (Hashtbl.data price_changes_to_banana_totals) |> Option.value_exn
;;

let () =
  let secret_nums = read () in
  let part1_ans = solve_part1 secret_nums in
  let part2_ans = solve_part2 secret_nums in
  printf "%d\n%d\n" part1_ans part2_ans
;;
