open Core

let n = 71 (* Set to 7 for sample input *)
let part1_block_count = 1028 (* Set to 12 for sample input *)
let start_x = 0
let start_y = 0
let end_x = n - 1
let end_y = n - 1
let dirs4 = [ 1, 0; 0, 1; -1, 0; 0, -1 ]
let dirs8 = [ 1, 0; 1, 1; 0, 1; -1, 1; -1, 0; -1, -1; 0, -1; 1, -1 ]

let read () =
  In_channel.(input_lines stdin)
  |> List.map ~f:(fun line ->
    String.split line ~on:','
    |> List.map ~f:Int.of_string
    |> function
    | [ x; y ] -> x, y
    | _ -> invalid_arg "Each line should contain exactly two comma-separated integers")
;;

let is_in_bounds x y = 0 <= x && x < n && 0 <= y && y < n

let get_neighbours dirs x y =
  List.filter_map dirs ~f:(fun (dx, dy) ->
    let x2 = x + dx in
    let y2 = y + dy in
    Option.some_if (is_in_bounds x2 y2) (x2, y2))
;;

let solve_part1 blocks =
  let visited = Array.make_matrix ~dimx:n ~dimy:n false in
  visited.(start_x).(start_y) <- true;
  List.take blocks part1_block_count
  |> List.iter ~f:(fun (x, y) -> visited.(x).(y) <- true);
  let queue = Queue.singleton (start_x, start_y) in
  let rec bfs steps =
    if visited.(end_x).(end_y)
    then steps
    else (
      for _ = 1 to Queue.length queue do
        let x, y = Queue.dequeue_exn queue in
        let neighbours = get_neighbours dirs4 x y in
        List.iter neighbours ~f:(fun (x2, y2) ->
          if not visited.(x2).(y2)
          then (
            visited.(x2).(y2) <- true;
            Queue.enqueue queue (x2, y2)))
      done;
      bfs (steps + 1))
  in
  bfs 0
;;

(* Gonna solve using Core's inbuilt Union_find to make things more exciting.
   Idea is to iterate over the bytes and find when they first connect the top and right walls
   to the bottom and left walls. Once this happens, the upper left space will be cut off
   from the bottom right. Union Find can be used to do this efficiently. *)
let solve_part2 blocks =
  let uf = Array.make_matrix ~dimx:n ~dimy:n None in
  (* Create special nodes to represent top and right walls as well as bottom and left walls *)
  let top_right_node = Union_find.create (n, -1) in
  let bottom_left_node = Union_find.create (-1, n) in
  let add_block (x, y) =
    let uf_node = Union_find.create (x, y) in
    uf.(x).(y) <- Some uf_node;
    if x = n - 1 || y = 0 then Union_find.union uf_node top_right_node;
    if x = 0 || y = n - 1 then Union_find.union uf_node bottom_left_node;
    let neighbours = get_neighbours dirs8 x y in
    List.iter neighbours ~f:(fun (x2, y2) ->
      Option.iter uf.(x2).(y2) ~f:(Union_find.union uf_node))
  in
  let final_block =
    List.find_exn blocks ~f:(fun block ->
      add_block block;
      Union_find.same_class top_right_node bottom_left_node)
  in
  sprintf "%d,%d" (fst final_block) (snd final_block)
;;

let () =
  let blocks = read () in
  let part1_ans = solve_part1 blocks in
  let part2_ans = solve_part2 blocks in
  printf "%d\n%s\n" part1_ans part2_ans
;;
