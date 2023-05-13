using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Wilderwood
{
    public class HexCellTerrain : MonoBehaviour
    {
        public HexCell hexCell;
        public MeshRenderer meshRenderer;
        public Material grasslandMaterial;
        public Material swampMaterial;
        public Material forestMaterial;
        public Material darkForestMaterial;
        public Material hillsMaterial;
        public Material mountainsMaterial;
        public Material waterMaterial;

        public void SetTerrainType(string terrainType)
        {
            switch (terrainType)
            {
                case "grassland":
                    meshRenderer.material = grasslandMaterial;
                    break;
                case "swamp":
                    meshRenderer.material = swampMaterial;
                    break;
                case "forest":
                    meshRenderer.material = forestMaterial;
                    break;
                case "dark forest":
                    meshRenderer.material = darkForestMaterial;
                    break;
                case "hills":
                    meshRenderer.material = hillsMaterial;
                    break;
                case "mountains":
                    meshRenderer.material = mountainsMaterial;
                    break;
                case "water":
                    meshRenderer.material = waterMaterial;
                    break;
            }
        }
    }
}