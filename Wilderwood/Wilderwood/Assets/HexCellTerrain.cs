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
        public Color color;

        public void SetTerrainType(string terrainType)
        {
            Material newMaterial = null;
            switch (terrainType)
            {
                case "grassland":
                    newMaterial = new Material(grasslandMaterial);
                    // Dark green
                    color = new Color(0.3529412f, 0.572549f, 0.345098f);
                    break;
                case "swamp":
                    newMaterial = new Material(swampMaterial);
                    // Lime green
                    color = new Color(0.909804f, 0.7098039f, 0.5294118f);
                    break;
                case "forest":
                    newMaterial = new Material(forestMaterial);
                    // fresh green
                    color = new Color(0.1803921f, 0.4666666f, 0.5215686f);
                    break;
                case "dark forest":
                    newMaterial = new Material(darkForestMaterial);
                    // Dark green
                    color = new Color(0.3764706f, 0.3294117f, 0.4039216f);
                    break;
                case "hills":
                    newMaterial = new Material(hillsMaterial);
                    // Blue grey
                    color = new Color(0.30f, 0.34f, 0.59f);
                    break;
                case "mountains":
                    newMaterial = new Material(mountainsMaterial);
                    // Grey
                    color = new Color(0.30f, 0.34f, 0.59f);

                    break;
                case "water":
                    newMaterial = new Material(waterMaterial);
                    // Blue
                    color = new Color(0.317647f, 0.5333333f, 0.6745098f);
                    break;
            }
            if (newMaterial != null)
            {
                newMaterial.mainTextureScale = new Vector2(0.5f, 0.5f);
                newMaterial.mainTextureOffset = new Vector2(0.25f, 0.25f);
                meshRenderer.material = newMaterial;
                // meshRenderer.material.color = color;
                // Asign the color to the submesh of the hexagon of the HexCell
                meshRenderer.materials[1].color = color;
            }
        }
    }
}