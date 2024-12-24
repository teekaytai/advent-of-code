open Core

let input_wire_prefixes = "xy"
let output_wire_prefix = "z"

type gate =
  | And
  | Or
  | Xor
[@@deriving equal]

type wire =
  | Input_wire of int
  | Gated_wire of gate * string * string

let is_input_wire name = String.contains input_wire_prefixes (String.get name 0)
let is_output_wire name = String.equal (String.prefix name 1) output_wire_prefix

let is_first_input_wire name =
  is_input_wire name && String.equal (String.suffix name 2) "00"
;;

let is_first_output_wire = String.equal (output_wire_prefix ^ "00")

let is_last_output_wire output_bit_count =
  String.equal (output_wire_prefix ^ Int.to_string (output_bit_count - 1))
;;

let apply_gate in_gate bit1 bit2 =
  match in_gate with
  | And -> bit1 land bit2
  | Or -> bit1 lor bit2
  | Xor -> bit1 lxor bit2
;;

let parse_gate = function
  | "AND" -> And
  | "OR" -> Or
  | "XOR" -> Xor
  | _ -> invalid_arg "Unknown gate type"
;;

let parse_input_wires =
  List.fold
    ~init:(Map.empty (module String))
    ~f:(fun acc line ->
      let name = String.slice line 0 (String.index_exn line ':') in
      let bit = Char.get_digit_exn (String.nget line (-1)) in
      Map.add_exn acc ~key:name ~data:(Input_wire bit))
;;

let parse_gated_wires lines =
  let add_wire_out_gate wire_name out_gate name_to_out_gates =
    Map.update name_to_out_gates wire_name ~f:(function
      | None -> [ out_gate ]
      | Some out_gates -> out_gate :: out_gates)
  in
  List.fold
    lines
    ~init:(Map.empty (module String), Map.empty (module String))
    ~f:(fun (name_to_gated_wires, name_to_out_gates) line ->
      match String.split ~on:' ' line with
      | [ in_wire_name_1; gate_name; in_wire_name_2; _; name ] ->
        let curr_gate = parse_gate gate_name in
        let gated_wire = Gated_wire (curr_gate, in_wire_name_1, in_wire_name_2) in
        let new_name_to_gated_wires =
          Map.add_exn name_to_gated_wires ~key:name ~data:gated_wire
        in
        let new_name_to_out_gates =
          name_to_out_gates
          |> add_wire_out_gate in_wire_name_1 curr_gate
          |> add_wire_out_gate in_wire_name_2 curr_gate
        in
        new_name_to_gated_wires, new_name_to_out_gates
      | _ -> invalid_arg "Invalid gate format")
;;

let find_output_bit_count = Map.counti ~f:(fun ~key:name ~data:_ -> is_output_wire name)

let read () =
  let lines = In_channel.(input_lines stdin) in
  let sep_idx = fst (List.findi_exn ~f:(fun _ line -> String.is_empty line) lines) in
  let name_to_input_wires = parse_input_wires (List.take lines sep_idx) in
  let name_to_gated_wires, name_to_out_gates =
    parse_gated_wires (List.drop lines (sep_idx + 1))
  in
  let name_to_wires = Map.merge_disjoint_exn name_to_input_wires name_to_gated_wires in
  let output_bit_count = find_output_bit_count name_to_gated_wires in
  name_to_wires, name_to_out_gates, output_bit_count
;;

let make_wire_bit_finder name_to_wires =
  let find_wire_bit rec_find_wire_bit name =
    match Map.find_exn name_to_wires name with
    | Input_wire bit -> bit
    | Gated_wire (in_gate, in_wire_name_1, in_wire_name_2) ->
      let bit1 = rec_find_wire_bit in_wire_name_1 in
      let bit2 = rec_find_wire_bit in_wire_name_2 in
      apply_gate in_gate bit1 bit2
  in
  Memo.recursive ~hashable:String.hashable find_wire_bit
;;

let solve_part1 name_to_wires =
  let find_wire_bit = make_wire_bit_finder name_to_wires in
  Map.fold_range_inclusive
    name_to_wires
    ~min:output_wire_prefix
    ~max:(output_wire_prefix ^ "99")
    ~init:0
    ~f:(fun ~key:name ~data:_ total ->
      let bit_idx = Int.of_string (String.suffix name 2) in
      let bit = find_wire_bit name in
      total + (bit lsl bit_idx))
;;

(* This function assumes wires only get swapped within their own full adder. *)
let is_incorrect_wire name_to_out_gates output_bit_count ~key:name ~data:curr_wire =
  (* Carry wires get their bits OR-ed together to feed into the next full adder. *)
  let is_carry_wire name =
    equal_gate (List.hd_exn (Map.find_exn name_to_out_gates name)) Or
  in
  let is_correct =
    match curr_wire with
    | Input_wire _ -> true
    | Gated_wire (in_gate, in_wire_name, _) ->
      if is_output_wire name
      then
        (* Output wires should be the XOR of intermediate wires, except the first output
           wire z00 which is the XOR of input wires x00 and y00, and the last output wire
           which is the OR of the last two carry bits. *)
        is_last_output_wire output_bit_count name
        || (equal_gate in_gate Xor
            && ((not (is_input_wire in_wire_name)) || is_first_output_wire name))
      else if is_carry_wire name
      then equal_gate in_gate And
      else (
        (* The remaining wires are the inputs to half-adders. They can be the OR of the
           carry bits from the previous adder, or the XOR of input bits from x and y.
           An edge case is the AND of the first input bits x00 and y00. *)
        match in_gate with
        | Or -> true
        | Xor -> is_input_wire in_wire_name && not (is_first_input_wire in_wire_name)
        | And -> is_first_input_wire in_wire_name)
  in
  not is_correct
;;

(* Notice that we do not need to identify the pairs to swap, we just need to detect
   incorrectly connected wires. *)
let solve_part2 name_to_wires name_to_out_gates output_bit_count =
  Map.filteri name_to_wires ~f:(is_incorrect_wire name_to_out_gates output_bit_count)
  |> Map.keys
  |> String.concat ~sep:","
;;

let () =
  let name_to_wires, name_to_out_gates, output_bit_count = read () in
  let part1_ans = solve_part1 name_to_wires in
  let part2_ans = solve_part2 name_to_wires name_to_out_gates output_bit_count in
  printf "%d\n%s\n" part1_ans part2_ans
;;
