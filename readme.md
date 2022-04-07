# Combinatorial Labelling Optimisation Algorithm

This repository contains an implementation of a multi-objective combinatorial labelling optimisation algorithm that uses decision trees for solution generation. The generated solutions are evaluated using inbuilt costing operators (kernels), weighted based on user-defined costing parameters. The best solution is then presented in the standard output, with all discovered solutions saved in a file. Because of the large number of possible solutions, the decision tree traversal algorithm provides pruning parameters that reduce the size of the explored space by discarding unfavourable solutions. 

## Terminology
The algorithm deals with two main types of entities - `nodes` and `labels`. 

* `Nodes` represent the "things" that the algorithm is trying to group; 
* `Labels` are the groups themselves. 

In job definitions, both nodes and labels can have attributes, such as strings, integers, arrays, and so on. These attributes are used by costing kernels (functionals) to produce a cost for a specific Node-Label pairing. 

`Costing kernels` are simply functions that receive two attributes from Nodes and Labels, and produce a number that constitutes the cost. Costing functionals are categorised by producing a cost for a Node-Node pairing, Node-Label pairing or Label-Label pairing, and further broken down into functionals evaluated before and during the algorithm execution. 

## Generating solution cost
As mentioned in the introduction, the algorithm uses a multi-objective approach to evaluating the solutions it generates. This is achieved through the use of costing kernels - costing kernels are functionals that operate on two properties from either Nodes or Labels or both. All costing kernels are contained within the `/src/modules/*_costing.py` files within the `calculatePostRunCost`, `calculateNodeToNodeCost`, `calculateRuntimeGroupToNodeCost` and `calculatePreRunGroupToNodeCost` functions. These functions are meant to be user-extensible, as they provide full access to Node and Label data entries.  

As mentioned before, there are two types of costing kernels:
* `pre-run kernels` - these costing kernels are run before the execution of the algorithm, caching the cost for pairing every entity with every other entity in their respective areas
* `runtime kernels` - these costing kernels are evaluated during the execution of the algorithm

## Solution evaluation order
The decision tree traversal function explores the tree in a top-down, left-to-right approach. This means that subject to effective pruning parameters, solutions from that area of the solution space will be favoured. Practically this is not a problem, as the distribution of solutions in the solution space is random, and users can force exploration of the full space by adjusting the pruning parameters of the algorithm.

![EvaluationOrder](https://user-images.githubusercontent.com/40371335/162235562-d65bcbb4-048c-491d-a3a9-8c571be22aab.png)


## Pruning parameters
As mentioned earlier, the algorithm provides pruning parameters to reduce the amount of the solution space it explores. These pruning rules are crucial to developing quick-running optimisation jobs because of the complexity of the algorithm. The pruning rules that the algorithm offers are as follows:

* `"TREE_PRUNE_TRESHOLD"` - this pruning rule determines the maximum cost of a branch in the decision tree before stopping its exploration
* `"STEP_MAX_COST"` -  this pruning rule determines the maximum cost of a single step in the decision - steps below that cost will be explored
* `"MINIMUM_ACCEPTABLE_SOLUTION` - this pruning rule indicates the minimum acceptable solution cost - the exploration of the decision tree will stop once a solution below this cost is discovered
* `"MAX_PATHS_PER_NODE"` - this pruning rule determines how many branches can be created at each step in the decision tree - when new branches are evaluated, only the best `MAX_PATHS_PER_NODE` branches will be explored, the rest being discarded
