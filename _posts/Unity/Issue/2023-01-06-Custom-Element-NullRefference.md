---
title: "Unity Android Build Issue ~dynamic_array"
categories: [Unity/Issue]
tag : ["Unity", "Custom VisualElement", "Null Refference Issue"]
---



# Unity 2021 Custom VisualElement Null Refference Exception

- Unity Version : 2021.3

- Custom 한 Visual Element를 UI Builder에서 사용시 오류 로그 발생

  - 컨트롤을 배치하고 내부 요소를 선택하면 오류 로그가 생김
  - 사용하는데 문제는 없었음

- ![image-20230106213758586](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106213758586.png)

- ```
  NullReferenceException: Object reference not set to an instance of an object
  Unity.UI.Builder.BuilderInspectorAttributes.RefreshAttributeField (UnityEngine.UIElements.BindableElement fieldElement) (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderInspectorAttributes.CreateAttributeRow (UnityEngine.UIElements.UxmlAttributeDescription attribute) (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderInspectorAttributes.GenerateAttributeFields () (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderInspectorAttributes.Refresh () (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderInspector.RefreshUI () (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderInspector.SelectionChanged () (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderSelection.NotifyOfSelectionChange (Unity.UI.Builder.IBuilderSelectionNotifier source) (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderSelection.AddToSelection (Unity.UI.Builder.IBuilderSelectionNotifier source, UnityEngine.UIElements.VisualElement ve, System.Boolean undo, System.Boolean sort) (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderSelection.AddToSelection (Unity.UI.Builder.IBuilderSelectionNotifier source, UnityEngine.UIElements.VisualElement ve) (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.BuilderExplorer.ElementSelectionChanged (System.Collections.Generic.List`1[T] elements) (at <f62cb1617a29470c88ea5593249ef206>:0)
  Unity.UI.Builder.ElementHierarchyView.OnSelectionChange (System.Collections.Generic.IEnumerable`1[T] items) (at <f62cb1617a29470c88ea5593249ef206>:0)
  UnityEngine.UIElements.InternalTreeView.OnSelectionChange (System.Collections.Generic.IEnumerable`1[T] selectedListItems) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.NotifyOfSelectionChange () (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.SetSelectionInternal (System.Collections.Generic.IEnumerable`1[T] indices, System.Boolean sendNotification) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.SetSelection (System.Collections.Generic.IEnumerable`1[T] indices) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.SetSelection (System.Int32 index) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.DoSelect (UnityEngine.Vector2 localPosition, System.Int32 clickCount, System.Boolean actionKey, System.Boolean shiftKey) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.ProcessPointerDown (UnityEngine.UIElements.IPointerEvent evt) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVerticalCollectionView.OnPointerDown (UnityEngine.UIElements.PointerDownEvent evt) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.EventCallbackFunctor`1[TEventType].Invoke (UnityEngine.UIElements.EventBase evt, UnityEngine.UIElements.PropagationPhase propagationPhase) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.EventCallbackRegistry.InvokeCallbacks (UnityEngine.UIElements.EventBase evt, UnityEngine.UIElements.PropagationPhase propagationPhase) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.CallbackEventHandler.HandleEvent (UnityEngine.UIElements.EventBase evt) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.EventDispatchUtilities.PropagateEvent (UnityEngine.UIElements.EventBase evt) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.PointerEventDispatchingStrategy.SendEventToTarget (UnityEngine.UIElements.EventBase evt) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.PointerEventDispatchingStrategy.DispatchEvent (UnityEngine.UIElements.EventBase evt, UnityEngine.UIElements.IPanel panel) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.EventDispatcher.ApplyDispatchingStrategies (UnityEngine.UIElements.EventBase evt, UnityEngine.UIElements.IPanel panel, System.Boolean imguiEventIsInitiallyUsed) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.EventDispatcher.ProcessEvent (UnityEngine.UIElements.EventBase evt, UnityEngine.UIElements.IPanel panel) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.EventDispatcher.Dispatch (UnityEngine.UIElements.EventBase evt, UnityEngine.UIElements.IPanel panel, UnityEngine.UIElements.DispatchMode dispatchMode) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.BaseVisualElementPanel.SendEvent (UnityEngine.UIElements.EventBase e, UnityEngine.UIElements.DispatchMode dispatchMode) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.UIElementsUtility.DoDispatch (UnityEngine.UIElements.BaseVisualElementPanel panel) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.UIElementsUtility.UnityEngine.UIElements.IUIElementsUtility.ProcessEvent (System.Int32 instanceID, System.IntPtr nativeEventPtr, System.Boolean& eventHandled) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.UIEventRegistration.ProcessEvent (System.Int32 instanceID, System.IntPtr nativeEventPtr) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.UIElements.UIEventRegistration+<>c.<.cctor>b__1_2 (System.Int32 i, System.IntPtr ptr) (at <e262c2d839014c8090373617ef295bab>:0)
  UnityEngine.GUIUtility.ProcessEvent (System.Int32 instanceID, System.IntPtr nativeEventPtr, System.Boolean& result) (at <67dcbe01fcb94a00b87487037550ce1c>:0)
  ```

  

# 미해결

- 해당 문제는 아직 해결되지 않은 것 같다.

- 사용상 큰 문제가 없고 최신 버전인 2022.2에서도 발생하는거 보면 중요하지 않다고 판단하고 후 순위로 밀렸을 지도...

- 아래는 Unity Forum 관련 내용

  ![image-20230106214218925](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106214218925.png)

![image-20230106214301675](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106214301675.png)

![image-20230106214322819](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106214322819.png)



# Ref

[https://forum.unity.com/threads/bug-in-ui-builder-nullref-when-building-custom-element-tree-from-uxml-unity-2021-2-6f1.1217169/](https://forum.unity.com/threads/bug-in-ui-builder-nullref-when-building-custom-element-tree-from-uxml-unity-2021-2-6f1.1217169/)