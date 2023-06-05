// HexagonalGrid.cs

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using GenericMenu = UnityEditor.GenericMenu;

namespace Wilderwood
{
    public class HexagonalGrid : MonoBehaviour
    {
        public int width = 3;
        public int height = 3;
        public float cellSize = 2;
        public GameObject cellPrefab;
        private Grid grid;
        public Grid Grid
        {
            get { return grid; }
        }
        public Vector2Int start = new Vector2Int(0, 0);
        public Vector2Int end = new Vector2Int(0, 0);
        List<GameObject> prefabs = new List<GameObject>();
        public HexCell selectedHexCell;

        // variable that can store the HexCell coordinates as strings 
        // (e.g. "0,0" for the bottom left cell, "0,1" for the cell to the right of that, etc.)
        public string coordinates;

        void Start()
        {
            grid = GetComponent<Grid>();
            start = new Vector2Int(9999, 9999);
            end = new Vector2Int(9999, 9999);
            selectedHexCell = null;
            UpdateGrid();
            foreach (GameObject prefab in prefabs)
            {
                if (prefab.GetComponent<HexCell>() != null)
                {
                    HexCell hexCell = prefab.GetComponent<HexCell>();
                    // Debug.Log("HexCell row: " + hexCell.row);
                    // Debug.Log("HexCell col: " + hexCell.col);
                    // Debug.Log("HexCell height: " + hexCell.height);
                    // add  the coordinates in the coordinates variable
                    coordinates += "(" + hexCell.row + "," + hexCell.col + "), ";
                    // add a line break after every row of hexagons
                    if (hexCell.col == width - 1)
                    {
                        coordinates += "\n";
                    }
                }
            }

        }

        void Update()
        {
            HandleEvents();
        }

        void UpdateGrid()
        {
            grid.cellSize = new Vector3(cellSize * 0.86f, cellSize, cellSize);
            foreach (Transform child in transform)
            {
                Destroy(child.gameObject);
            }

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    Vector3Int cellPosition = new Vector3Int(x, y, 0);
                    Vector3 worldPosition = grid.CellToWorld(cellPosition);
                    GameObject prefab = Instantiate(cellPrefab, worldPosition, Quaternion.identity, transform);
                    HexCell hexCell = prefab.GetComponent<HexCell>();
                    hexCell.Initialize();
                    hexCell.row = y;
                    hexCell.col = x;
                    prefabs.Add(prefab);
                }
            }

            float[,] prefabHeights = new float[width, height];
            for (int i = 0; i < prefabs.Count; i++)
            {
                float height = prefabs[i].GetComponent<Renderer>().bounds.size.y;
                int x = i % width;
                int y = i / width;
                prefabHeights[x, y] = height;
            }
        }
        Vector2Int SelectHexagon(Vector3 worldPos)
        {
            float minDistance = float.MaxValue;
            HexCell closestHex = null;
            foreach (GameObject prefab in prefabs)
            {
                HexCell hexCell = prefab.GetComponent<HexCell>();
                Vector3 centerPos = hexCell.transform.position;

                float distance = Vector3.Distance(worldPos, centerPos);
                if (distance < minDistance)
                {
                    minDistance = distance;
                    closestHex = hexCell;
                }
            }
            if (closestHex != null)
            {
                return new Vector2Int(closestHex.col, closestHex.row);

            }
            else
            {
                return new Vector2Int(99999, 99999); ;
            }
        }
        public HexCell GetHexCell(int row, int col)
        {
            foreach (GameObject prefab in prefabs)
            {
                HexCell hexCell = prefab.GetComponent<HexCell>();
                if (hexCell.row == row && hexCell.col == col)
                {
                    return hexCell;
                }
            }
            return null;
        }
        void HandleEvents()
        {
            if (Input.GetMouseButtonDown(0))
            {
                Vector3 mousePos = Input.mousePosition;
                Ray ray = Camera.main.ScreenPointToRay(mousePos);
                // RaycastHit hit;
                RaycastHit[] hits = new RaycastHit[1];
                int numHits = Physics.RaycastNonAlloc(ray, hits, 100.0f); // set a maximum distance for the raycast
                if (numHits > 0)
                {
                    // the ray hit something, so we can get the information from the first hit in the array
                    RaycastHit hit = hits[0];

                    // do something with the hit information...
                    if (Physics.Raycast(ray, out hit))
                    {
                        Vector3 worldPos = hit.point;
                        Vector2Int hex = SelectHexagon(worldPos);

                        if (hex != null)
                        {
                            if (start == new Vector2Int(9999, 9999) && end == new Vector2Int(9999, 9999))
                            {
                                SetStartHex(hex);
                            }
                            else if (start != new Vector2Int(9999, 9999) && end == new Vector2Int(9999, 9999))
                            {
                                SetEndHex(hex);
                                List<Vector2Int> path = Pathfinding.AStarHex(grid, start, end, height, width);
                                if (path != null)
                                {
                                    string pathString = "";
                                    foreach (Vector2Int pathHex in path)
                                    {
                                        pathString += pathHex + ", ";
                                    }
                                    // Debug.Log("Start: " + start);
                                    // Debug.Log("Path: " + pathString);
                                    // Debug.Log("End: " + end);
                                }
                                else
                                {
                                    // Debug.Log("No path found");
                                }
                                ResetCoordinates();
                            }
                            else
                            {
                                ResetCoordinates();
                            }
                        }
                        else
                        {
                            // Debug.Log("No hexagon selected");
                        }
                    }
                }
            }

            if (Input.GetMouseButtonDown(0))
            {
                Vector3 mousePos = Input.mousePosition;
                Ray ray = Camera.main.ScreenPointToRay(mousePos);

                RaycastHit[] hits = new RaycastHit[1];
                int numHits = Physics.RaycastNonAlloc(ray, hits, 100.0f); // set a maximum distance for the raycast

                if (numHits > 0)
                {
                    // the ray hit something, so we can get the information from the first hit in the array
                    RaycastHit hit = hits[0];
                    // Debug.Log("Hit: " + hit.collider.gameObject.name);
                    // do something with the hit information...
                }
            }
            if (Input.GetMouseButtonDown(1))
            {
                Vector3 mousePos = Input.mousePosition;
                Ray ray = Camera.main.ScreenPointToRay(mousePos);
                RaycastHit hit;
                if (Physics.Raycast(ray, out hit))
                {
                    Vector3 worldPos = hit.point;
                    Vector2Int hex = SelectHexagon(worldPos);
                    if (hit.collider.gameObject.GetComponent<HexCell>() != null)
                    {
                        HexCell hexCell = hit.collider.gameObject.GetComponent<HexCell>();
                        if (hexCell != null)
                        {
                            selectedHexCell = GetHexCell(hex.x, hex.y);
                            Debug.Log("Selected hexagon: " + hexCell.row + ", " + hexCell.col);
                        }
                    }
                }
            }
        }
        void SetStartHex(Vector2Int hex)
        {
            start = hex;
        }

        void SetEndHex(Vector2Int hex)
        {
            end = hex;
        }

        void ResetCoordinates()
        {
            start = new Vector2Int(9999, 9999);
            end = new Vector2Int(9999, 9999);
        }
    }
}
