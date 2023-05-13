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
        // public void Initialize()
        // {
        //     // Assign a random terrain type to the HexCell
        //     string[] terrainTypes = new string[] { "grassland", "swamp", "forest", "dark forest", "hills", "mountains", "water" };
        //     int randomIndex = Random.Range(0, terrainTypes.Length);
        //     string randomTerrainType = terrainTypes[randomIndex];
        //     hexCellTerrain.SetTerrainType(randomTerrainType);

        //     // Create a new material and assign it to the renderer
        //     Material material = new Material(Shader.Find("Standard"));
        //     material.mainTextureScale = new Vector2(0.5f, 0.5f);
        //     material.mainTextureOffset = new Vector2(0.25f, 0.25f);

        //     // Set the main texture of the material based on the terrain type
        //     switch (randomTerrainType)
        //     {
        //         case "grassland":
        //             material.mainTexture = Resources.Load<Texture>("Textures/grassland");
        //             break;
        //         case "swamp":
        //             material.mainTexture = Resources.Load<Texture>("Textures/swamp");
        //             break;
        //         case "forest":
        //             material.mainTexture = Resources.Load<Texture>("Textures/forest");
        //             break;
        //         case "dark forest":
        //             material.mainTexture = Resources.Load<Texture>("Textures/dark_forest");
        //             break;
        //         case "hills":
        //             material.mainTexture = Resources.Load<Texture>("Textures/hills");
        //             break;
        //         case "mountains":
        //             material.mainTexture = Resources.Load<Texture>("Textures/mountains");
        //             break;
        //         case "water":
        //             material.mainTexture = Resources.Load<Texture>("Textures/water");
        //             break;
        //     }

        //     GetComponent<Renderer>().material = material;
        // }


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
