open Core

type button = char [@@deriving compare, sexp_of, hash]

module Action = struct
  type t = int * button * button [@@deriving compare, sexp_of, hash]
end

let num_dpads_part1 = 3
let num_dpads_part2 = 26
let left = '<'
let down = 'v'
let right = '>'
let up = '^'
let a_btn = 'A'
let numpad_gap = 3, 0
let dpad_gap = 0, 0

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

let fold_pairwise lst ~first ~init ~f =
  List.fold lst ~init:(init, first) ~f:(fun (acc, prev) curr -> f acc prev curr, curr)
  |> fst
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

let read () =
  In_channel.(input_lines stdin)
  |> List.map ~f:(fun line ->
    String.to_list line, Int.of_string (String.drop_suffix line 1))
;;

(** Returns possible lists of directional keypad button pushes needed to move from the
    start position to the end position and then press the button at the end.
    Each possible sequence only changes direction at most once since this is always
    quicker for a higher level robot/human to perform.
    Sequences avoid causing a robot to move over the gap. *)
let find_dpad_seqs ~gap:(gap_r, gap_c) (start_r, start_c) (end_r, end_c) =
  let dr = end_r - start_r in
  let dc = end_c - start_c in
  let vert_dpad_list = List.init (abs dr) ~f:(fun _ -> if dr > 0 then down else up) in
  let horiz_dpad_list = List.init (abs dc) ~f:(fun _ -> if dc > 0 then right else left) in
  let vert_then_horiz_seq = vert_dpad_list @ horiz_dpad_list @ [ a_btn ] in
  let horiz_then_vert_seq = horiz_dpad_list @ vert_dpad_list @ [ a_btn ] in
  if dr = 0 || dc = 0
  then [ vert_then_horiz_seq ] (* Both sequences are identical *)
  else if start_r = gap_r && end_c = gap_c
  then [ vert_then_horiz_seq ]
  else if start_c = gap_c && end_r = gap_r
  then [ horiz_then_vert_seq ]
  else [ vert_then_horiz_seq; horiz_then_vert_seq ]
;;

let find_dpad_seqs_for_dpad = find_dpad_seqs ~gap:dpad_gap
let find_dpad_seqs_for_numpad = find_dpad_seqs ~gap:numpad_gap

(** Computes the minimum number of button pushes required to move a robot from the start
    button to another button and push that button with num_dpads intermediate directional
    keypads. rec_min_steps is the function that will count the steps for the robot one
    level higher. *)
let min_steps rec_min_steps btn_to_pos find_dpad_seqs (num_dpads, start_btn, btn_to_push) =
  match num_dpads with
  | 0 -> 1
  | _ ->
    let min_steps_dpad_seq =
      fold_pairwise ~first:a_btn ~init:0 ~f:(fun total curr_btn next_btn ->
        total + rec_min_steps (num_dpads - 1, curr_btn, next_btn))
    in
    let start_pos = Hashtbl.find_exn btn_to_pos start_btn in
    let end_pos = Hashtbl.find_exn btn_to_pos btn_to_push in
    find_dpad_seqs start_pos end_pos
    |> List.map ~f:min_steps_dpad_seq
    |> List.min_elt ~compare
    |> Option.value_exn
;;

let min_steps_dpad rec_min_steps_dpad =
  min_steps rec_min_steps_dpad dpad_btn_to_pos find_dpad_seqs_for_dpad
;;

let memo_min_steps_dpad = memoize_rec (module Action) min_steps_dpad

let min_steps_numpad =
  min_steps memo_min_steps_dpad numpad_btn_to_pos find_dpad_seqs_for_numpad
;;

let min_steps_numpad_seq num_dpads code =
  fold_pairwise code ~first:a_btn ~init:0 ~f:(fun total curr_btn next_btn ->
    total + min_steps_numpad (num_dpads, curr_btn, next_btn))
;;

let compute_complexity num_dpads (code, value) =
  value * min_steps_numpad_seq num_dpads code
;;

let solve_part1 = List.sum (module Int) ~f:(compute_complexity num_dpads_part1)
let solve_part2 = List.sum (module Int) ~f:(compute_complexity num_dpads_part2)

let () =
  let code_value_pairs = read () in
  let part1_ans = solve_part1 code_value_pairs in
  let part2_ans = solve_part2 code_value_pairs in
  printf "%d\n%d\n" part1_ans part2_ans
;;
