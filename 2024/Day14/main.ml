open Core

let width = 101
let height = 103
let mid_x = width / 2
let mid_y = height / 2
let time_to_bathroom = 100

type robot =
  { x : int
  ; y : int
  ; dx : int
  ; dy : int
  }

type point =
  { x : int
  ; y : int
  }

let get_x { x; _ } = x
let get_y { y; _ } = y

(** Finds x, y and g such that a*x + b*y = g = gcd(a, b) *)
let rec bezout a b =
  match b with
  | 0 -> 1, 0, a
  | _ ->
    let x1, y1, g = bezout b (a mod b) in
    y1, x1 - (y1 * (a / b)), g
;;

(** Finds the smallest positive x such that x = r1 (mod m1) and x = r2 (mod m2).
    m1 and m2 must be coprime *)
let chinese_remainder_theorem ~r1 ~m1 ~r2 ~m2 =
  let x1, x2, g = bezout m1 m2 in
  if g <> 1
  then invalid_arg "Moduli must be coprime"
  else ((r1 * x2 * m2) + (r2 * x1 * m1)) % (m1 * m2)
;;

let mean n xs = List.sum (module Float) xs ~f:Fn.id /. Float.of_int n

let variance n xs =
  let xs_floats = List.map xs ~f:Float.of_int in
  let mean_x = mean n xs_floats in
  mean
    n
    (List.map xs_floats ~f:(fun x ->
       let x_diff = x -. mean_x in
       x_diff *. x_diff))
;;

let robot_pos_at_time { x; y; dx; dy } ~time =
  { x = (x + (dx * time)) % width; y = (y + (dy * time)) % height }
;;

let get_quadrant { x; y } =
  assert (x >= 0 && y >= 0);
  if x = mid_x || y = mid_y
  then None
  else (
    match x > mid_x, y > mid_y with
    | false, false -> Some 0
    | true, false -> Some 1
    | false, true -> Some 2
    | true, true -> Some 3)
;;

let read () =
  let re_nums = Re.Perl.compile_pat {|-?\d+|} in
  let match_to_int _match = Int.of_string (Re.Group.get _match 0) in
  In_channel.(input_lines stdin)
  |> List.map ~f:(fun line ->
    match Re.all re_nums line with
    | [ match_x; match_y; match_dx; match_dy ] ->
      { x = match_to_int match_x
      ; y = match_to_int match_y
      ; dx = match_to_int match_dx
      ; dy = match_to_int match_dy
      }
    | _ -> invalid_arg "Robot should be defined with exactly 4 integers")
;;

let solve_part1 robots =
  let quadrant_totals = [| 0; 0; 0; 0 |] in
  List.iter robots ~f:(fun robot ->
    get_quadrant (robot_pos_at_time robot ~time:time_to_bathroom)
    |> Option.iter ~f:(fun quadrant ->
      quadrant_totals.(quadrant) <- succ quadrant_totals.(quadrant)));
  Array.fold quadrant_totals ~init:1 ~f:Int.( * )
;;

(* Fully automated solution based on this post:
   https://www.reddit.com/r/adventofcode/comments/1he0asr/2024_day_14_part_2_why_have_fun_with_image *)
let solve_part2 robots =
  let num_robots = List.length robots in
  let find_variances_at_time time =
    let points = List.map robots ~f:(robot_pos_at_time ~time) in
    let x_variance = variance num_robots (List.map points ~f:get_x) in
    let y_variance = variance num_robots (List.map points ~f:get_y) in
    (x_variance, time), (y_variance, time)
  in
  let compare_var_time_pairs = Tuple2.compare ~cmp1:Float.compare ~cmp2:Int.compare in
  let find_min_var_time variance_series =
    List.min_elt variance_series ~compare:compare_var_time_pairs
    |> Option.value_exn
    |> snd
  in
  let x_variance_series, y_variance_series =
    List.range 0 (max width height) |> List.map ~f:find_variances_at_time |> List.unzip
  in
  let min_x_var_time = find_min_var_time x_variance_series in
  let min_y_var_time = find_min_var_time y_variance_series in
  chinese_remainder_theorem ~r1:min_x_var_time ~m1:width ~r2:min_y_var_time ~m2:height
;;

let () =
  let robots = read () in
  let part1_ans = solve_part1 robots in
  let part2_ans = solve_part2 robots in
  printf "%d\n%d\n" part1_ans part2_ans
;;
