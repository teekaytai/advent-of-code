open Core

let max_len = 9

type chunk =
  { start : int
  ; len : int
  }

type file =
  { id : int
  ; chunk : chunk
  }

let cmp_gaps gap1 gap2 = gap1.start - gap2.start

let file_checksum { id; chunk = { start; len } } =
  id * (len * (start + start + len - 1) / 2)
;;

let read_and_parse () =
  In_channel.(input_line_exn stdin)
  |> String.to_list
  |> List.fold_mapi ~init:0 ~f:(fun i total_len digit ->
    let len = Char.get_digit_exn digit in
    let chunk = { start = total_len; len } in
    total_len + len, (i, chunk))
  |> snd
  |> List.partition_map ~f:(fun (i, chunk) ->
    if i % 2 = 0 then First { id = i / 2; chunk } else Second chunk)
;;

(* Return the newly moved file as well as any partial file/gap left behind after the move *)
let move_file_into_gap file gap =
  let { id; chunk = { start = file_start; len = file_len } } = file in
  let { start = gap_start; len = gap_len } = gap in
  let min_len = Int.min file_len gap_len in
  let moved_file = { id; chunk = { start = gap_start; len = min_len } } in
  let opt_leftover_file =
    if file_len > min_len
    then Some { id; chunk = { start = file_start; len = file_len - min_len } }
    else None
  in
  let opt_leftover_gap =
    if gap_len > min_len
    then Some { start = gap_start + min_len; len = gap_len - min_len }
    else None
  in
  moved_file, opt_leftover_file, opt_leftover_gap
;;

let solve_part1 files gaps =
  let rec loop files gaps checksum =
    match files with
    | [] -> checksum
    | file :: files_tail ->
      (match gaps with
       | [] -> loop files_tail gaps checksum + file_checksum file
       | gap :: _ when gap.start > file.chunk.start ->
         loop files_tail gaps checksum + file_checksum file
       | gap :: gaps_tail ->
         let moved_file, opt_leftover_file, opt_leftover_gap =
           move_file_into_gap file gap
         in
         let new_files =
           Option.value_map opt_leftover_file ~default:files_tail ~f:(fun leftover_file ->
             leftover_file :: files_tail)
         in
         let new_gaps =
           Option.value_map opt_leftover_gap ~default:gaps_tail ~f:(fun leftover_gap ->
             leftover_gap :: gaps_tail)
         in
         loop new_files new_gaps checksum + file_checksum moved_file)
  in
  loop (List.rev files) gaps 0
;;

let solve_part2 files gaps =
  let len_to_gaps_pq =
    Array.init (max_len + 1) ~f:(fun _ -> Pairing_heap.create ~cmp:cmp_gaps ())
  in
  List.iter gaps ~f:(fun gap -> Pairing_heap.add len_to_gaps_pq.(gap.len) gap);
  let find_earliest_usuable_gap file =
    Array.foldi len_to_gaps_pq ~init:None ~f:(fun len opt_earliest_gap gap_pq ->
      if len < file.chunk.len || Pairing_heap.is_empty gap_pq
      then opt_earliest_gap
      else (
        let gap = Pairing_heap.top_exn gap_pq in
        if gap.start > file.chunk.start
        then opt_earliest_gap
        else (
          match opt_earliest_gap with
          | Some earliest_gap when cmp_gaps earliest_gap gap < 0 -> opt_earliest_gap
          | _ -> Some gap)))
  in
  List.fold_right files ~init:0 ~f:(fun file checksum ->
    match find_earliest_usuable_gap file with
    | None -> checksum + file_checksum file
    | Some gap ->
      ignore (Pairing_heap.pop_exn len_to_gaps_pq.(gap.len));
      let moved_file, _, opt_leftover_gap = move_file_into_gap file gap in
      Option.iter opt_leftover_gap ~f:(fun leftover_gap ->
        Pairing_heap.add len_to_gaps_pq.(leftover_gap.len) leftover_gap);
      checksum + file_checksum moved_file)
;;

let () =
  let files, gaps = read_and_parse () in
  let part1_ans = solve_part1 files gaps in
  let part2_ans = solve_part2 files gaps in
  printf "%d\n%d\n" part1_ans part2_ans
;;
