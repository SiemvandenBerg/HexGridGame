
// Unit.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Wilderwood
{
    public class Unit : MonoBehaviour
    {
        public float speed = 5f;
        private bool isSelected = false;
        public GameObject gridObject;
        public HexagonalGrid hexagonalGrid;
        Grid grid;
        public Vector2Int start = new Vector2Int(0, 0);
        public Vector2Int end = new Vector2Int(0, 0);
        public int row;
        public int col;
        public int rows;
        public int cols;
        int hopHeight = 1;
        void Start()
        {
            gridObject = GameObject.Find("GridObject");
            hexagonalGrid = gridObject.GetComponent<HexagonalGrid>();
            grid = hexagonalGrid.Grid;
            HexCell hexCellZero = grid.GetComponentsInChildren<HexCell>()[0];
            Vector3 worldPosition = hexCellZero.transform.position;
            float height = hexCellZero.height;
            worldPosition += new Vector3(0, height, 0);
            transform.position = worldPosition;
            Vector3Int cellPosition = grid.WorldToCell(worldPosition);
            HexCell hexCell = grid.GetComponentsInChildren<HexCell>()[0];
            row = hexCell.row;
            col = hexCell.col;
            cols = hexagonalGrid.width;
            rows = hexagonalGrid.height;
        }
        void Update()
        {
            if (isSelected)
            {
                if (Input.GetMouseButtonDown(0))
                {
                    Vector3 mousePos = Input.mousePosition;
                    Ray ray = Camera.main.ScreenPointToRay(mousePos);
                    RaycastHit hit;

                    // get the world position of the unit 
                    Vector3 unitWorldPos = transform.position;
                    Vector3Int unitCellPosition = grid.WorldToCell(unitWorldPos);
                    Vector2Int unitHex = new Vector2Int(unitCellPosition.x, unitCellPosition.y);

                    // set the start hex to the unit's hex
                    start = unitHex;

                    if (Physics.Raycast(ray, out hit))
                    {
                        Vector3 worldPos = hit.point;
                        Vector3Int cellPosition = grid.WorldToCell(worldPos);
                        Vector2Int hex = new Vector2Int(cellPosition.x, cellPosition.y);
                        end = hex;
                        // Get the HexCell at the specified row and col
                        HexCell hexCell = hexagonalGrid.GetHexCell(cellPosition.y, cellPosition.x);
                        if (hexCell != null)
                        {
                            // Debug.Log("HexCell row: " + hexCell.row);
                        }

                    }
                }
                if (end != Vector2Int.zero && Input.GetMouseButtonDown(0))
                {
                    List<Vector2Int> path = Pathfinding.AStarHex(grid, start, end, rows, cols);
                    List<Vector4> worldPath = new List<Vector4>();
                    foreach (Vector2Int cellPosition in path)
                    {
                        Vector3 worldPosition = grid.CellToWorld(new Vector3Int(cellPosition.x, cellPosition.y, 0));
                        HexCell hexCell = hexagonalGrid.GetHexCell(cellPosition.y, cellPosition.x);
                        float height = hexCell != null ? hexCell.height : 0;
                        worldPath.Add(new Vector4(worldPosition.x, worldPosition.y, worldPosition.z, height));
                    }
                    StartCoroutine(MoveAlongPath(worldPath));
                }
            }
        }
        IEnumerator MoveAlongPath(List<Vector4> path)
        {
            for (int i = 0; i < path.Count; i++)
            {
                Vector3 startPos = new Vector3(path[i].x, path[i].y, path[i].z);
                float startHeight = path[i].w;
                Vector3 endPos = i < path.Count - 1 ? new Vector3(path[i + 1].x, path[i + 1].y, path[i + 1].z) : startPos;
                float endHeight = i < path.Count - 1 ? path[i + 1].w : startHeight;
                float journeyLength = Vector3.Distance(startPos, endPos);

                float startTime = Time.time;
                float distCovered = 0;
                while (distCovered < journeyLength)
                {
                    distCovered = (Time.time - startTime) * speed;
                    float fracJourney = distCovered / journeyLength;
                    // transform.position = Vector3.Lerp(startPos, endPos, fracJourney); // without easing
                    transform.position = Vector3.Lerp(startPos, endPos, fracJourney * fracJourney * (3f - 2f * fracJourney));
                    transform.position += new Vector3(0, Mathf.Sin(fracJourney * Mathf.PI) * hopHeight + Mathf.Lerp(startHeight, endHeight + 0.01f, fracJourney), 0);
                    if (fracJourney >= 1f) // if the end of the path has been reached, break out of the loop
                    {
                        DeselectUnit(); // this aint right, it deselects after every step in the path. Fix later
                        break;
                    }
                    yield return null;
                }
            }
        }
        void OnMouseDown()
        {
            SelectUnit();
        }
        public void SelectUnit()
        {
            isSelected = true;
            Debug.Log("Unit selected");
        }
        public void DeselectUnit()
        {
            isSelected = false;
            Debug.Log("Unit deselected");
        }
    }
}