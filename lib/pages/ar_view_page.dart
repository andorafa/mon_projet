
import 'package:ar_flutter_plugin/datatypes/config_planedetection.dart';
import 'package:ar_flutter_plugin/datatypes/node_types.dart';
import 'package:ar_flutter_plugin/managers/ar_anchor_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_location_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_object_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_session_manager.dart';
import 'package:ar_flutter_plugin/models/ar_anchor.dart';
import 'package:ar_flutter_plugin/models/ar_hittest_result.dart';
import 'package:ar_flutter_plugin/models/ar_node.dart';
import 'package:flutter/material.dart';
import 'package:ar_flutter_plugin/ar_flutter_plugin.dart';
import 'package:vector_math/vector_math_64.dart';
import 'dart:math' as math;

class ARViewPage extends StatefulWidget {
  final String? modelUrl;

  const ARViewPage({Key? key, this.modelUrl}) : super(key: key);

  @override
  State<ARViewPage> createState() => _ARViewPageState();
}

class _ARViewPageState extends State<ARViewPage> {
  late ARSessionManager _arSessionManager;
  late ARObjectManager _arObjectManager;
  late ARAnchorManager _arAnchorManager;

  ARNode? _currentNode;
  ARPlaneAnchor? _currentAnchor;
  static const String _nodeName = 'productARNode';

  @override
  void dispose() {
    _arSessionManager.dispose();
    super.dispose();
  }

  void onARViewCreated(
      ARSessionManager sessionManager,
      ARObjectManager objectManager,
      ARAnchorManager anchorManager,
      ARLocationManager locationManager,
      ) {
    _arSessionManager = sessionManager;
    _arObjectManager = objectManager;
    _arAnchorManager = anchorManager;

    _arSessionManager.onInitialize(
      showFeaturePoints: false,
      showPlanes: true,
      customPlaneTexturePath: "",
      handleTaps: true,
    );
    _arObjectManager.onInitialize();

    _arSessionManager.onPlaneOrPointTap = _onPlaneTap;
  }

  Future<void> _onPlaneTap(List<ARHitTestResult> hits) async {
    if (hits.isEmpty) return;

    if (widget.modelUrl == null || widget.modelUrl!.isEmpty) {
      _arSessionManager.onError("Aucune URL de modèle 3D fournie.");
      return;
    }

    final hit = hits.first;

    if (_currentNode != null) {
      await _arObjectManager.removeNode(_currentNode!);
      _currentNode = null;
    }

    final anchor = ARPlaneAnchor(transformation: hit.worldTransform);
    final anchorAdded = await _arAnchorManager.addAnchor(anchor);
    if (anchorAdded != true) {
      _arSessionManager.onError("Échec création ancrage");
      return;
    }
    _currentAnchor = anchor;

    final node = ARNode(
      name: _nodeName,
      type: NodeType.webGLB,
      uri: widget.modelUrl!,
      scale: Vector3(0.4, 0.4, 0.4),
      position: Vector3.zero(),
      eulerAngles: Vector3.zero(),
    );

    final nodeAdded = await _arObjectManager.addNode(node, planeAnchor: anchor);
    if (nodeAdded == true) {
      _currentNode = node;
    } else {
      _arSessionManager.onError("Échec d'ajout du modèle");
    }
  }

  void _scaleCurrentNode(double factor) {
    if (_currentNode == null) return;
    final s = _currentNode!.scale;
    _currentNode!.scale = Vector3(s.x * factor, s.y * factor, s.z * factor);
  }

  void _yawCurrentNode(double degrees) {
    if (_currentNode == null) return;
    final delta = degrees * (math.pi / 180);
    final current = _currentNode!.eulerAngles;
    _currentNode!.eulerAngles = Vector3(current.x, current.y + delta, current.z);
  }

  void _pitchCurrentNode(double degrees) {
    if (_currentNode == null) return;
    final delta = degrees * (math.pi / 180);
    final current = _currentNode!.eulerAngles;
    _currentNode!.eulerAngles = Vector3(current.x + delta, current.y, current.z);
  }

  void _translateCurrentNode2D(Vector2 delta) {
    if (_currentNode == null) return;
    final pos = _currentNode!.position;
    _currentNode!.position = Vector3(
      pos.x + delta.x,
      pos.y + delta.y,
      pos.z,
    );
  }

  void _translateCurrentNodeDepth(double deltaZ) {
    if (_currentNode == null) return;
    final pos = _currentNode!.position;
    _currentNode!.position = Vector3(
      pos.x,
      pos.y,
      pos.z + deltaZ,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Vue AR')),
      body: Stack(
        children: [
          ARView(
            onARViewCreated: onARViewCreated,
            planeDetectionConfig: PlaneDetectionConfig.horizontal,
          ),
          Positioned(
            bottom: 20,
            right: 20,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                FloatingActionButton(
                  heroTag: 'scale_up',
                  mini: true,
                  onPressed: () => _scaleCurrentNode(1.2),
                  child: const Icon(Icons.zoom_in),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'scale_down',
                  mini: true,
                  onPressed: () => _scaleCurrentNode(0.8),
                  child: const Icon(Icons.zoom_out),
                ),
                const SizedBox(height: 16),
                FloatingActionButton(
                  heroTag: 'yaw_left',
                  mini: true,
                  onPressed: () => _yawCurrentNode(-15),
                  child: const Icon(Icons.rotate_left),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'yaw_right',
                  mini: true,
                  onPressed: () => _yawCurrentNode(15),
                  child: const Icon(Icons.rotate_right),
                ),
                const SizedBox(height: 16),
                FloatingActionButton(
                  heroTag: 'pitch_up',
                  mini: true,
                  onPressed: () => _pitchCurrentNode(-15),
                  child: const Icon(Icons.arrow_upward),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'pitch_down',
                  mini: true,
                  onPressed: () => _pitchCurrentNode(15),
                  child: const Icon(Icons.arrow_downward),
                ),
              ],
            ),
          ),
          Positioned(
            bottom: 20,
            left: 20,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                FloatingActionButton(
                  heroTag: 'forward',
                  mini: true,
                  onPressed: () => _translateCurrentNodeDepth(0.05),
                  child: const Icon(Icons.upload),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'backward',
                  mini: true,
                  onPressed: () => _translateCurrentNodeDepth(-0.05),
                  child: const Icon(Icons.download),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'up',
                  mini: true,
                  onPressed: () => _translateCurrentNode2D(Vector2(0, 0.05)),
                  child: const Icon(Icons.keyboard_arrow_up),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'down',
                  mini: true,
                  onPressed: () => _translateCurrentNode2D(Vector2(0, -0.05)),
                  child: const Icon(Icons.keyboard_arrow_down),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'left',
                  mini: true,
                  onPressed: () => _translateCurrentNode2D(Vector2(-0.05, 0)),
                  child: const Icon(Icons.keyboard_arrow_left),
                ),
                const SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'right',
                  mini: true,
                  onPressed: () => _translateCurrentNode2D(Vector2(0.05, 0)),
                  child: const Icon(Icons.keyboard_arrow_right),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
