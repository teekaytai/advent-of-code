open Core

module Node = struct
  module T = struct
    type t = string [@@deriving compare, sexp_of]
  end

  include T
  include Comparator.Make (T)
end

let parse_edge line =
  match String.split ~on:'-' line with
  | [ u; v ] -> u, v
  | _ -> invalid_arg "Edge should connect exactly two nodes"
;;

let add_directed_edge node_from node_to graph =
  Map.update graph node_from ~f:(function
    | None -> Set.singleton (module Node) node_to
    | Some adj_set -> Set.add adj_set node_to)
;;

let add_undirected_edge node_u node_v graph =
  graph |> add_directed_edge node_u node_v |> add_directed_edge node_v node_u
;;

let read () =
  In_channel.(fold_lines stdin)
    ~init:(Map.empty (module Node))
    ~f:(fun graph line ->
      let node_u, node_v = parse_edge line in
      add_undirected_edge node_u node_v graph)
;;

(* Identify the nodes in each clique in alphabetical order to avoid double counting. *)
let solve_part1 graph =
  Map.sumi
    (module Int)
    graph
    ~f:(fun ~key:node_u ~data:adjs_u ->
      Set.sum
        (module Int)
        adjs_u
        ~f:(fun node_v ->
          Set.count adjs_u ~f:(fun node_w ->
            let adjs_v = Map.find_exn graph node_v in
            Set.mem adjs_v node_w
            && List.exists [ node_u; node_v; node_w ] ~f:(String.is_prefix ~prefix:"t")
            && Node.compare node_u node_v < 0
            && Node.compare node_v node_w < 0)))
;;

(* Simplified version of the Bron–Kerbosch algorithm that doesn't maintain the set X of
   already processed nodes, since we are only interested in finding the maximum clique,
   not every maximal clique. *)
let find_max_clique graph =
  let get_neighbours = Map.find_exn graph in
  let rec loop curr_clique potential_nodes =
    if Set.is_empty potential_nodes
    then curr_clique
    else (
      let node = Set.choose_exn potential_nodes in
      let max_clique_with_node =
        loop (Set.add curr_clique node) (Set.inter potential_nodes (get_neighbours node))
      in
      let max_clique_wo_node = loop curr_clique (Set.remove potential_nodes node) in
      if Set.length max_clique_with_node >= Set.length max_clique_wo_node
      then max_clique_with_node
      else max_clique_wo_node)
  in
  loop (Set.empty (module Node)) (Map.key_set graph)
;;

let solve_part2 graph = find_max_clique graph |> Set.to_list |> String.concat ~sep:","

let () =
  let graph = read () in
  let part1_ans = solve_part1 graph in
  let part2_ans = solve_part2 graph in
  printf "%d\n%s\n" part1_ans part2_ans
;;
