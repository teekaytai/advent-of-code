open Core

let trail_len = 10
let dirs = [ -1, 0; 0, 1; 1, 0; 0, -1 ]

let count_unique lst =
  lst
  |> List.dedup_and_sort ~compare:(Tuple2.compare ~cmp1:Int.compare ~cmp2:Int.compare)
  |> List.length
;;

let is_in_bounds grid r c =
  0 <= r && r < Array.length grid && 0 <= c && c < Array.length grid.(0)
;;

let read () =
  Array.of_list_map
    In_channel.(input_lines stdin)
    ~f:(fun r -> Array.map (String.to_array r) ~f:Char.get_digit_exn)
;;

let bfs grid start_r start_c =
  let rec loop step frontier =
    match frontier with
    | [] -> 0, 0
    | _ when step = trail_len -> count_unique frontier, List.length frontier
    | _ ->
      let new_frontier =
        List.concat_map frontier ~f:(fun (r, c) ->
          List.filter_map dirs ~f:(fun (dr, dc) ->
            let r2 = r + dr in
            let c2 = c + dc in
            if is_in_bounds grid r2 c2 && grid.(r2).(c2) = step
            then Some (r2, c2)
            else None))
      in
      loop (step + 1) new_frontier
  in
  loop 1 [ start_r, start_c ]
;;

let solve grid =
  Array.foldi grid ~init:(0, 0) ~f:(fun r (total1, total2) row ->
    Array.foldi row ~init:(total1, total2) ~f:(fun c (subtotal1, subtotal2) cell ->
      match cell with
      | 0 ->
        let trailhead_score, trailhead_rating = bfs grid r c in
        subtotal1 + trailhead_score, subtotal2 + trailhead_rating
      | _ -> subtotal1, subtotal2))
;;

let () =
  let grid = read () in
  let part1_ans, part2_ans = solve grid in
  printf "%d\n%d\n" part1_ans part2_ans
;;
