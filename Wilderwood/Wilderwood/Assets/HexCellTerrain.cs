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
            Material newMaterial = null;
            switch (terrainType)
            {
                case "grassland":
                    newMaterial = new Material(grasslandMaterial);
                    break;
                case "swamp":
                    newMaterial = new Material(swampMaterial);
                    break;
                case "forest":
                    newMaterial = new Material(forestMaterial);
                    break;
                case "dark forest":
                    newMaterial = new Material(darkForestMaterial);
                    break;
                case "hills":
                    newMaterial = new Material(hillsMaterial);
                    break;
                case "mountains":
                    newMaterial = new Material(mountainsMaterial);
                    break;
                case "water":
                    newMaterial = new Material(waterMaterial);
                    break;
            }
            if (newMaterial != null)
            {
                newMaterial.mainTextureScale = new Vector2(0.5f, 0.5f);
                newMaterial.mainTextureOffset = new Vector2(0.25f, 0.25f);
                meshRenderer.material = newMaterial;
            }
        }

    }
}