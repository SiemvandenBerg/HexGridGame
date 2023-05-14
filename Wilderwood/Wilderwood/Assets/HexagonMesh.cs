using UnityEngine;

namespace Wilderwood
{
    public class HexagonMesh : MonoBehaviour
    {
        private Mesh mesh;
        private int topHexagonVerticesCount = 6;
        private float heightFactor;
        float hexagonHeight = 0.5f;
        private void Awake()
        {
            mesh = new Mesh();
            MeshCollider meshCollider = gameObject.AddComponent<MeshCollider>();
            GetComponent<MeshFilter>().mesh = mesh;
            float heightFactor = Random.Range(0.1f, 0.5f);
            heightFactor = Mathf.Round(heightFactor * 100f) / 100f;
            hexagonHeight += heightFactor;
            Vector3[] vertices = new Vector3[]
            {
                // Bottom hexagon
                new Vector3(-Mathf.Sqrt(3f) / 2f, 0f, -0.5f),
                new Vector3(0f, 0f, -1f),
                new Vector3(Mathf.Sqrt(3f) / 2f, 0f, -0.5f),
                new Vector3(Mathf.Sqrt(3f) / 2f, 0f, 0.5f),
                new Vector3(0f, 0f, 1f),
                new Vector3(-Mathf.Sqrt(3f) / 2f, 0f, 0.5f),

                // Top hexagon
                new Vector3(-Mathf.Sqrt(3f) / 2f, hexagonHeight, -0.5f),
                new Vector3(0f, hexagonHeight, -1f),
                new Vector3(Mathf.Sqrt(3f) / 2f, hexagonHeight, -0.5f),
                new Vector3(Mathf.Sqrt(3f) / 2f, hexagonHeight, 0.5f),
                new Vector3(0f, hexagonHeight, 1f),
                new Vector3(-Mathf.Sqrt(3f) / 2f, hexagonHeight, 0.5f),
            };

            int[] triangles = new int[]
            {
                // Bottom hexagon
                0, 1, 5,
                1, 4, 5,
                1, 2, 4,
                2, 3, 4,

                // Top hexagon
                6, 11, 7,
                7, 11, 10,
                7, 10, 8,
                8, 10, 9,

                // Sides
                5, 6, 0,
                5, 11, 6,
                5, 4, 11,
                10, 11, 4,
                4, 3, 10,
                9, 10, 3,
                3, 2, 9,
                8, 9, 2,
                2, 1, 8,
                7, 8, 1,
                7, 1, 0,
                6, 7, 0,
            };

            mesh.vertices = vertices;
            mesh.triangles = triangles;
            mesh.RecalculateNormals();
            mesh.RecalculateBounds();

            Vector2[] uv = new Vector2[vertices.Length];

            // Set the UV coordinates of all vertices except those that correspond to the top hexagon to zero
            for (int i = 0; i < vertices.Length - topHexagonVerticesCount; i++)
            {
                uv[i] = Vector2.zero;
            }
            // Set the UV coordinates of the top vertices to correspond to the texture
            for (int i = vertices.Length - topHexagonVerticesCount; i < vertices.Length; i++)
            {
                uv[i] = new Vector2(vertices[i].x + 0.5f, vertices[i].z + 0.5f);
            }
            // Assign the UV coordinates to the mesh
            mesh.uv = uv;
            Material material = GetComponent<Renderer>().material;
            material.mainTextureScale = new Vector2(0.5f, 0.5f);
            material.mainTextureOffset = new Vector2(0.25f, 0.25f);
            material.mainTexture.wrapMode = TextureWrapMode.Clamp;

            HexCell hexCell = GetComponent<HexCell>();
            if (hexCell != null)
            {
                hexCell.height = hexagonHeight;
            }

            meshCollider.sharedMesh = mesh;
            // Create a new material
            Material topMaterial = new Material(Shader.Find("Standard"));
            // set color to light grey
            topMaterial.color = new Color(0.75f, 0.75f, 0.75f, 1f);

            // Get the mesh renderer component
            MeshRenderer meshRenderer = GetComponent<MeshRenderer>();
            // Get the current materials array
            Material[] materials = meshRenderer.materials;
            // Resize the materials array to add the new material
            System.Array.Resize(ref materials, materials.Length + 1);
            // Assign the new material to the last element of the materials array
            materials[materials.Length - 1] = topMaterial;
            // Assign the new materials array back to the mesh renderer
            meshRenderer.materials = materials;

            // Create a new submesh for the top hexagon
            mesh.subMeshCount = 2;
            // int[] topTriangles = new int[] { 6, 11, 7, 7, 11, 10, 7, 10, 8, 8, 10, 9 };
            // mesh.SetTriangles(topTriangles, 1);
            int[] sideTriangles = new int[] { 5, 6, 0, 5, 11, 6, 5, 4, 11, 10, 11, 4, 4, 3, 10, 9, 10, 3, 3, 2, 9, 8, 9, 2, 2, 1, 8, 7, 8, 1, 7, 1, 0, 6, 7, 0 };
            mesh.SetTriangles(sideTriangles, 1);
        }
    }
}