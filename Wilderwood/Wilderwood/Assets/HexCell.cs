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

        public string randomTerrainType;
        public GameObject construction;
        public GameObject unit;
        public GameObject resource;
        public GameObject obstacle;
        public GameObject terrain;
        public HexCellTerrain hexCellTerrain;
        // Get the gameobject quad called Terrain that is attached to the same gameobject as this script
        public GameObject terrainQuad;


        void Awake()
        {
            gridObject = GameObject.Find("GridObject");
            hexagonalGrid = gridObject.GetComponent<HexagonalGrid>();
            grid = hexagonalGrid.Grid;
            hexCellTerrain = GetComponent<HexCellTerrain>();
            hexagonMesh = GetComponentInChildren<HexagonMesh>();
            terrainQuad = transform.Find("Terrain").gameObject;
            terrainQuad.transform.position = new Vector3(terrainQuad.transform.position.x, height, terrainQuad.transform.position.z);
        }

        void Start()
        {
        }

        public void Initialize()
        {
            // Assign a random terrain type to the HexCell
            string[] terrainTypes = new string[] { "grassland", "swamp", "forest", "dark forest", "hills", "mountains", "water" };
            int randomTerrainTypeIndex = Random.Range(0, terrainTypes.Length);
            randomTerrainType = terrainTypes[randomTerrainTypeIndex];
            hexCellTerrain.SetTerrainType(randomTerrainType);

            // Load all textures from the "Textures" folder into an array
            Texture2D[] textures = Resources.LoadAll<Texture2D>("Textures");
            Debug.Log("Textures: " + textures.Length);

            // Select a random index from the array
            int randomTerrainTextureIndex = Random.Range(0, textures.Length);

            // Get the selected texture
            Texture2D randomTexture = textures[randomTerrainTextureIndex];

            // Apply the texture to the terrain
            terrainQuad.GetComponent<Renderer>().material.mainTexture = randomTexture;
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
