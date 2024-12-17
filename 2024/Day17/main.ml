open Core

let bxl_opcode = 1

type state =
  { instruction_id : int
  ; reg_a : int
  ; reg_b : int
  ; reg_c : int
  ; output : int list
  }

let read_register () =
  In_channel.(input_line_exn stdin)
  |> String.split ~on:' '
  |> List.last_exn
  |> Int.of_string
;;

let read_program () =
  In_channel.(input_line_exn stdin)
  |> String.split ~on:' '
  |> List.last_exn
  |> String.split ~on:','
  |> Array.of_list_map ~f:Int.of_string
;;

let read () =
  let init_reg_a = read_register () in
  let init_reg_b = read_register () in
  let init_reg_c = read_register () in
  assert (String.is_empty In_channel.(input_line_exn stdin));
  let program = read_program () in
  init_reg_a, init_reg_b, init_reg_c, program
;;

let execute_step program curr_state =
  let { instruction_id; reg_a; reg_b; reg_c; output } = curr_state in
  let op = program.(instruction_id) in
  let operand = program.(instruction_id + 1) in
  let temp_next_state = { curr_state with instruction_id = instruction_id + 2 } in
  let combo_operand () =
    match operand with
    | 0 | 1 | 2 | 3 -> operand
    | 4 -> reg_a
    | 5 -> reg_b
    | 6 -> reg_c
    | _ -> invalid_argf "Invalid combo operand: %d" operand ()
  in
  match op with
  | 0 -> { temp_next_state with reg_a = reg_a asr combo_operand () }
  | 1 -> { temp_next_state with reg_b = reg_b lxor operand }
  | 2 -> { temp_next_state with reg_b = combo_operand () % 8 }
  | 3 when reg_a = 0 -> temp_next_state
  | 3 when reg_a <> 0 -> { curr_state with instruction_id = operand }
  | 4 -> { temp_next_state with reg_b = reg_b lxor reg_c }
  | 5 -> { temp_next_state with output = (combo_operand () % 8) :: output }
  | 6 -> { temp_next_state with reg_b = reg_a asr combo_operand () }
  | 7 -> { temp_next_state with reg_c = reg_a asr combo_operand () }
  | _ -> invalid_argf "Invalid opcode: %d" op ()
;;

let run program start_state =
  let rec loop curr_state =
    if curr_state.instruction_id >= Array.length program
    then List.rev curr_state.output
    else loop (execute_step program curr_state)
  in
  loop start_state
;;

let solve_part1 program init_reg_a init_reg_b init_reg_c =
  let start_state =
    { instruction_id = 0
    ; reg_a = init_reg_a
    ; reg_b = init_reg_b
    ; reg_c = init_reg_c
    ; output = []
    }
  in
  let output = run program start_state in
  String.concat ~sep:"," (List.map ~f:Int.to_string output)
;;

let find_possible_a program bxl_operand_1 bxl_operand_2 =
  let rec dfs prog_idx reg_a =
    if prog_idx < 0
    then Some reg_a
    else
      Sequence.find_map (Sequence.range 0 8) ~f:(fun reg_b ->
        if reg_a = 0 && reg_b = 0
        then None
        else (
          let new_a = (reg_a lsl 3) + reg_b in
          let temp_b = reg_b lxor bxl_operand_1 in
          let reg_c = new_a asr temp_b in
          let output_val = temp_b lxor reg_c lxor bxl_operand_2 % 8 in
          if output_val = program.(prog_idx) then dfs (prog_idx - 1) new_a else None))
  in
  dfs (Array.length program - 1) 0
;;

let solve_part2 program =
  let bxl_operands =
    Array.filteri program ~f:(fun idx _ ->
      idx > 0 && idx % 2 = 1 && program.(idx - 1) = bxl_opcode)
  in
  let bxl_operand_1, bxl_operand_2 =
    match bxl_operands with
    | [| x; y |] -> x, y
    | _ -> failwith "Expected program to have exactly two bxl operations"
  in
  Option.value_exn (find_possible_a program bxl_operand_1 bxl_operand_2)
;;

let () =
  let init_reg_a, init_reg_b, init_reg_c, program = read () in
  let part1_ans = solve_part1 program init_reg_a init_reg_b init_reg_c in
  let part2_ans = solve_part2 program in
  printf "%s\n%d\n" part1_ans part2_ans
;;
