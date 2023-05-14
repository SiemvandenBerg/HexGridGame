using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

namespace Wilderwood
{
    public class HexCell : MonoBehaviour
    {
        public GameObject gridObject;
        Grid grid;
        public HexagonalGrid hexagonalGrid;
        public float height;
        public HexagonMesh hexagonMesh;
        public int row;
        public int col;
        public GameObject construction;
        public GameObject unit;
        public GameObject resource;
        public GameObject obstacle;
        public GameObject terrain;

        private HexCellTerrain hexCellTerrain;

        void Awake()
        {
            gridObject = GameObject.Find("GridObject");
            hexagonalGrid = gridObject.GetComponent<HexagonalGrid>();
            grid = hexagonalGrid.Grid;

            hexCellTerrain = GetComponent<HexCellTerrain>();
        }

        void Start()
        {
        }

        public void Initialize()
        {
            // Assign a random terrain type to the HexCell
            string[] terrainTypes = new string[] { "grassland", "swamp", "forest", "dark forest", "hills", "mountains", "water" };
            int randomIndex = Random.Range(0, terrainTypes.Length);
            string randomTerrainType = terrainTypes[randomIndex];
            hexCellTerrain.SetTerrainType(randomTerrainType);
        }

        public void BuildConstruction()
        {
            Debug.Log("Build Construction");
        }

        public void BuildUnit()
        {
            Debug.Log("Build Unit");
        }

        public void AddResource()
        {
            Debug.Log("Add Resource");
        }

        public void AddObstacle()
        {
            Debug.Log("Add Obstacle");
        }

        public void AddTerrain()
        {
            Debug.Log("Add Terrain");
        }
    }
}
