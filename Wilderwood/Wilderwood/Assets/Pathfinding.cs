// My coordinate system is represented like this on the game screen: 
// (7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7);
// (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7); 
// (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7); 
// (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7); 
// (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7); 
// (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7); 
// (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7); 
// (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7);

// The pathfinding works well when moving up on the grid (eg from (1,2) to (6,5). But when it moves down on the grid, the movement skips cells and makes non-economic moves:

using System.Collections.Generic;
using UnityEngine;
using System.Linq;

namespace Wilderwood
{
    public static class Pathfinding
    {
        public static List<Vector2Int> AStarHex(Grid grid, Vector2Int start, Vector2Int end, int width, int height)
        {
            var heap = new List<(float, Vector2Int)>();
            heap.Add((0, start));
            var parents = new Dictionary<Vector2Int, Vector2Int?>();
            var costs = new Dictionary<Vector2Int, float>();
            var priorities = new Dictionary<Vector2Int, float>();
            costs[start] = 0;
            priorities[start] = 0;
            parents[start] = null;
            float currentCost = 0;
            while (heap.Count > 0)
            {
                heap.Sort((x, y) => x.Item1.CompareTo(y.Item1));
                Vector2Int currentNode;
                (currentCost, currentNode) = heap[0];
                heap.RemoveAt(0);
                // Debug.Log($"Current node: {currentNode}, Current cost: {currentCost}");
                if (currentNode == end)
                {
                    var path = new List<Vector2Int> { currentNode };
                    while (parents.ContainsKey(currentNode))
                    {
                        if (parents[currentNode].HasValue)
                        {
                            currentNode = parents[currentNode].Value;
                            path.Add(currentNode);
                        }
                        else
                        {
                            break;
                        }
                    }
                    path.Reverse();
                    // path.RemoveAt(path.Count - 1); // why was this here?
                    return path;
                }
                foreach (Vector2Int neighbor in GetNeighbors(grid, currentNode, width, height))
                {
                    float newCost = costs[currentNode] + HexCost(currentNode, neighbor);
                    if (!costs.ContainsKey(neighbor) || newCost < costs[neighbor])
                    {
                        costs[neighbor] = newCost;
                        parents[neighbor] = currentNode;
                        float heuristicCost = HexChebyshevDistance(neighbor, end);
                        float priority = newCost + heuristicCost;
                        if (!priorities.ContainsKey(neighbor) || priority < priorities[neighbor])
                        {
                            heap.RemoveAll(t => t.Item2 == neighbor);
                            heap.Add((priority, neighbor));
                            priorities[neighbor] = priority;
                        }
                    }
                }
            }
            return new List<Vector2Int>();
        }
        private static Vector3Int HexToCube(Vector2Int hex)
        {
            int x = hex.x;
            int z = hex.y;
            int y = -x - z;
            return new Vector3Int(x, y, z);
        }
        public static float HexCost(Vector2Int from, Vector2Int to)
        {
            return 1;
        }

        private static IEnumerable<Vector2Int> GetNeighbors(Grid grid, Vector2Int currentCell, int width, int height)
        {
            Vector2Int[] neighborOffsets;
            string neighbors = "";

            if (currentCell.y % 2 == 0)
            {
                // Even row
                neighborOffsets = new Vector2Int[]
                {
                    new Vector2Int(-1, 0), // West
                    new Vector2Int(1, 0), // East
                    new Vector2Int(-1, -1), // Northwest
                    new Vector2Int(0, -1), // Northeast
                    new Vector2Int(-1, 1), // Southwest
                    new Vector2Int(0, 1), // Southeast
                };
            }
            else
            {
                // Odd row
                neighborOffsets = new Vector2Int[]
                {
                    new Vector2Int(-1, 0), // West
                    new Vector2Int(1, 0), // East
                    new Vector2Int(0, -1), // Northwest
                    new Vector2Int(1, -1), // Northeast
                    new Vector2Int(0, 1), // Southwest
                    new Vector2Int(1, 1), // Southeast
                };
            }

            foreach (Vector2Int offset in neighborOffsets)
            {
                Vector2Int neighbor = currentCell + offset;
                // Check if the neighbor is within the bounds of the grid
                if (neighbor.x >= 0 && neighbor.x < width && neighbor.y >= 0 && neighbor.y < height)
                {
                    yield return neighbor;
                }
                // add the coordinates in the neighbors variable
                neighbors += "(" + neighbor.x + "," + neighbor.y + "), ";
            }
            // Debug.Log("Neighbors: " + neighbors);
        }
        private static float HexChebyshevDistance(Vector2Int a, Vector2Int b)
        {
            int dx = Mathf.Abs(a.x - b.x);
            int dy = Mathf.Abs(a.y - b.y);
            return Mathf.Max(dx, dy);
        }
    }
}
