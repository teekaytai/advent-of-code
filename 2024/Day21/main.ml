(* This solution is essentially a faster version of the dp solution which relies on an
   additional observation on how to choose the best path to take when moving between buttons.
   By using a matrix exponenitation trick, the solution can even be found in O(log n) time
   time instead of O(n) time (where n is the number of robots). *)
open Core

type button = char [@@deriving compare, sexp_of, hash]

(* A button pair represents moving from the first button to the second button and pressing it. *)
module Action = struct
  type t = button * button [@@deriving compare, sexp_of, hash]
end

let num_dpads_part1 = 3
let num_dpads_part2 = 26
let left = '<'
let down = 'v'
let right = '>'
let up = '^'
let a_btn = 'A'
let dpad_buttons = [ left; down; right; up; a_btn ]
let actions = List.cartesian_product dpad_buttons dpad_buttons
let num_actions = List.length actions
let numpad_gap = 3, 0
let dpad_gap = 0, 0

let actions_to_id =
  Hashtbl.of_alist_exn (module Action) (List.mapi actions ~f:(fun i action -> action, i))
;;

let dpad_btn_to_pos =
  Hashtbl.of_alist_exn
    (module Char)
    [ up, (0, 1); a_btn, (0, 2); left, (1, 0); down, (1, 1); right, (1, 2) ]
;;

let numpad_btn_to_pos =
  Hashtbl.of_alist_exn
    (module Char)
    [ '7', (0, 0)
    ; '8', (0, 1)
    ; '9', (0, 2)
    ; '4', (1, 0)
    ; '5', (1, 1)
    ; '6', (1, 2)
    ; '1', (2, 0)
    ; '2', (2, 1)
    ; '3', (2, 2)
    ; '0', (3, 1)
    ; 'A', (3, 2)
    ]
;;

let iter_pairwise lst ~first ~f =
  List.zip_exn (first :: List.drop_last_exn lst) lst |> List.iter ~f
;;

let map_pairwise lst ~first ~f =
  List.zip_exn (first :: List.drop_last_exn lst) lst |> List.map ~f
;;

let matrix_sum_rows = Array.map ~f:(fun row -> [| Array.sum (module Int) row ~f:Fn.id |])

let matrix_mul mat_a mat_b =
  let product =
    Array.make_matrix ~dimx:(Array.length mat_a) ~dimy:(Array.length mat_b.(0)) 0
  in
  Array.iteri mat_a ~f:(fun r row ->
    Array.iteri row ~f:(fun k num_a ->
      if num_a <> 0
      then
        Array.iteri mat_b.(k) ~f:(fun c num_b ->
          product.(r).(c) <- product.(r).(c) + (num_a * num_b))));
  product
;;

let matrix_pow mat exp =
  let n = Array.length mat in
  let identity = Array.make_matrix ~dimx:n ~dimy:n 0 in
  for i = 0 to n - 1 do
    identity.(i).(i) <- 1
  done;
  let rec loop mat exp acc =
    match exp with
    | 0 -> acc
    | _ when exp % 2 = 0 -> loop (matrix_mul mat mat) (exp / 2) acc
    | _ -> loop (matrix_mul mat mat) (exp / 2) (matrix_mul acc mat)
  in
  loop mat exp identity
;;

let read () =
  In_channel.(input_lines stdin)
  |> List.map ~f:(fun line ->
    String.to_list line, Int.of_string (String.drop_suffix line 1))
;;

(* Compare the column values of the first button in each sequence. *)
let compare_dpad_seq seq1 seq2 =
  let c1 = snd (Hashtbl.find_exn dpad_btn_to_pos (List.hd_exn seq1)) in
  let c2 = snd (Hashtbl.find_exn dpad_btn_to_pos (List.hd_exn seq2)) in
  Int.compare c1 c2
;;

(* This solution uses the insight that for any given movement from one dpad button to
   another, there is one path that is always optimal. Firstly we should keep changes
   in direction to a minimum. If still tied, we choose the sequence that goes to the
   leftmost button first. Since the left button is furthest from the A button, we should
   favour sequences that do all their leftward movement at once at the start, as opposed
   to potentially making multiple separate leftward movements when changing from one arrow
   button to another. *)
let find_dpad_seq ~gap:(gap_r, gap_c) (start_r, start_c) (end_r, end_c) =
  let dr = end_r - start_r in
  let dc = end_c - start_c in
  let vert_dpad_list = List.init (abs dr) ~f:(fun _ -> if dr > 0 then down else up) in
  let horiz_dpad_list = List.init (abs dc) ~f:(fun _ -> if dc > 0 then right else left) in
  let vert_then_horiz_seq = vert_dpad_list @ horiz_dpad_list @ [ a_btn ] in
  let horiz_then_vert_seq = horiz_dpad_list @ vert_dpad_list @ [ a_btn ] in
  if dr = 0 || dc = 0
  then vert_then_horiz_seq (* Both sequences are identical *)
  else if start_r = gap_r && end_c = gap_c
  then vert_then_horiz_seq
  else if start_c = gap_c && end_r = gap_r
  then horiz_then_vert_seq
  else if compare_dpad_seq vert_then_horiz_seq horiz_then_vert_seq < 0
  then vert_then_horiz_seq
  else horiz_then_vert_seq
;;

(** Returns an array counting how many of each of the 25 types of actions a higher level
    robot needs to do to get the current robot to move from the start button and push a
    target button. *)
let find_action_counts ~btn_to_pos ~gap (start_btn, btn_to_push) =
  let action_counts = Array.init num_actions ~f:(fun _ -> 0) in
  let start_pos = Hashtbl.find_exn btn_to_pos start_btn in
  let end_pos = Hashtbl.find_exn btn_to_pos btn_to_push in
  let dpad_seq = find_dpad_seq ~gap start_pos end_pos in
  iter_pairwise dpad_seq ~first:a_btn ~f:(fun action ->
    let new_action_id = Hashtbl.find_exn actions_to_id action in
    action_counts.(new_action_id) <- action_counts.(new_action_id) + 1);
  action_counts
;;

(** Computes a transition matrix that when multiplied with the column vector of action counts
    gives the action counts of the robot one level higher. *)
let precompute_transition_matrix () =
  let find_action_counts_for_dpad =
    find_action_counts ~btn_to_pos:dpad_btn_to_pos ~gap:dpad_gap
  in
  let mat = Array.of_list_map actions ~f:find_action_counts_for_dpad in
  Array.transpose_exn mat
;;

let get_transition_matrix = Memo.unit precompute_transition_matrix

(** Counts the actions needed by the robot controlling the numeric keypad robot so that
    the numeric keypad robot enters the given code. Returns the counts as a column vector *)
let code_to_action_counts code =
  let find_action_counts_for_numpad =
    find_action_counts ~btn_to_pos:numpad_btn_to_pos ~gap:numpad_gap
  in
  let action_counts_mat =
    map_pairwise code ~first:a_btn ~f:find_action_counts_for_numpad |> Array.of_list
  in
  matrix_sum_rows (Array.transpose_exn action_counts_mat)
;;

(** Finds the minimum steps required for the human to enter the code into the numeric keypad
    via num_dpads intermediate directional keypads. *)
let min_steps num_dpads code =
  code_to_action_counts code
  |> matrix_mul (matrix_pow (get_transition_matrix ()) (num_dpads - 1))
  |> Array.transpose_exn
  |> matrix_sum_rows
  |> fun mat -> mat.(0).(0)
;;

let compute_complexity num_dpads (code, value) = value * min_steps num_dpads code
let solve_part1 = List.sum (module Int) ~f:(compute_complexity num_dpads_part1)
let solve_part2 = List.sum (module Int) ~f:(compute_complexity num_dpads_part2)

let () =
  let code_value_pairs = read () in
  let part1_ans = solve_part1 code_value_pairs in
  let part2_ans = solve_part2 code_value_pairs in
  printf "%d\n%d\n" part1_ans part2_ans
;;
