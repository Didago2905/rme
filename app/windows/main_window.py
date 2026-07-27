from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.use_cases.analyze_media_use_case import (
    AnalyzeMediaUseCase,
)
from app.use_cases.import_series_use_case import (
    ImportSeriesUseCase,
)
from app.use_cases.scan_library import (
    ScanLibraryUseCase,
)
from app.use_cases.validate_media_use_case import (
    ValidateMediaUseCase,
)
from app.widgets.header_widget import HeaderWidget
from app.widgets.import_preview_widget import (
    ImportPreviewWidget,
)
from app.widgets.library_panel_widget import (
    LibraryPanelWidget,
)
from app.widgets.media_inspector_widget import (
    MediaInspectorWidget,
)
from core.models.parsed_episode import ParsedEpisode


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "R.I.T.M.O. Media Engine"
        )

        self.resize(
            1200,
            800,
        )

        self.setMinimumSize(
            900,
            600,
        )

        self._build_ui()

        #
        # Use Cases
        #

        self.scan_library_use_case = (
            ScanLibraryUseCase()
        )

        self.import_series_use_case = (
            ImportSeriesUseCase()
        )

        self.analyze_media_use_case = (
            AnalyzeMediaUseCase()
        )

        self.validate_media_use_case = (
            ValidateMediaUseCase()
        )

        self._connect_signals()

    def _build_ui(self) -> None:
        """
        Construye la estructura base de la ventana.
        """

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        self.main_layout.setSpacing(
            16
        )

        central_widget.setLayout(
            self.main_layout
        )

        self.header = HeaderWidget()

        self.library_panel = (
            LibraryPanelWidget()
        )

        self.import_preview = (
            ImportPreviewWidget()
        )

        self.media_inspector = (
            MediaInspectorWidget()
        )

        #
        # Workspace
        #

        self.workspace = QSplitter(
            Qt.Horizontal
        )

        self.workspace.setChildrenCollapsible(
            False
        )

        self.workspace.addWidget(
            self.import_preview
        )

        self.workspace.addWidget(
            self.media_inspector
        )

        self.workspace.setStretchFactor(
            0,
            1,
        )

        self.workspace.setStretchFactor(
            1,
            3,
        )

        self.workspace.setSizes(
            [
                380,
                820,
            ]
        )

        self.main_layout.addWidget(
            self.header
        )

        self.main_layout.addWidget(
            self.library_panel
        )

        self.main_layout.addWidget(
            self.workspace,
            1,
        )

    def _connect_signals(
        self,
    ) -> None:
        """
        Conecta las señales de la interfaz.
        """

        self.library_panel.scan_requested.connect(
            self._scan_library
        )

        self.library_panel.import_series_requested.connect(
            self._import_series
        )

        self.import_preview.item_selected.connect(
            self._on_item_selected
        )

    def _scan_library(
        self,
        library_path: str,
    ) -> None:
        """
        Atiende la solicitud de escaneo de la biblioteca.
        """

        metadata = (
            self.scan_library_use_case.execute(
                library_path
            )
        )

        print(
            metadata
        )

    def _import_series(
        self,
        series_path: str,
    ) -> None:
        """
        Atiende la solicitud de importación de una serie.
        """

        metadata = (
            self.import_series_use_case.execute(
                series_path
            )
        )

        self.import_preview.load_series(
            metadata
        )

    def _on_item_selected(
        self,
        item,
    ) -> None:
        """
        Atiende el cambio de selección del árbol.
        """

        selected = item.data(
            0,
            Qt.UserRole,
        )

        if not isinstance(
            selected,
            ParsedEpisode,
        ):
            self.media_inspector.show_item(
                selected
            )
            return

        media = (
            self.analyze_media_use_case.execute(
                selected.media_item.path
            )
        )

        validation = (
            self.validate_media_use_case.execute(
                media
            )
        )

        self.media_inspector.show_episode(
            selected,
            media,
            validation,
        )