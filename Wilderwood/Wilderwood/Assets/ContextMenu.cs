using UnityEngine;
using UnityEngine.UI;

namespace Wilderwood
{
    public class ContextMenu : MonoBehaviour
    {
        public GameObject gridObject;
        Grid grid;
        public HexagonalGrid hexagonalGrid;
        HexCell selectedHexCell;
        HexCell previousSelectedHexCell;
        GameObject panel;
        CanvasGroup panelGroup;

        void Awake()
        {
            gridObject = GameObject.Find("GridObject");
            hexagonalGrid = gridObject.GetComponent<HexagonalGrid>();
            grid = hexagonalGrid.Grid;
            panel = gameObject;
            panelGroup = panel.GetComponent<CanvasGroup>();
        }
        void Update()
        {
            if (hexagonalGrid.selectedHexCell != null)
            {
                if (hexagonalGrid.selectedHexCell != previousSelectedHexCell)
                {
                    panelGroup.alpha = 0;
                    previousSelectedHexCell = hexagonalGrid.selectedHexCell;
                    ShowMenuAtMousePosition();
                }

            }
            else
            {
                panelGroup.alpha = 0;
            }
            // panelGroup.alpha = 0;

        }

        void ShowMenuAtMousePosition()
        {
            if (panel != null && panelGroup.alpha == 0)
            {
                panelGroup.alpha = 1;
                panelGroup.transform.position = Input.mousePosition;
            }
        }

        public void BuildConstruction()
        {
            selectedHexCell.BuildConstruction();
        }

        public void BuildUnit()
        {
            selectedHexCell.BuildUnit();
        }

        public void AddResource()
        {
            selectedHexCell.AddResource();
        }

        public void AddObstacle()
        {
            selectedHexCell.AddObstacle();
        }

        public void AddTerrain()
        {
            selectedHexCell.AddTerrain();
        }

    }
}

