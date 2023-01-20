# VisualElement - Event

- VisualElement의 이벤트 시스템에 대한 기본적인 정리



## Event Process

- UI Toolkit은 EventDispatcher를 사용하여 Visual Element에 이벤트를 전달한다

- 전반적인 방식은 아래와 같다

![](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/UIElementsEvents.png)

```
TrickleDown : 이벤트가 발생하면 루트에서 시작하여 대상이되는 엘리먼트를 탐색한다
Target : 대상을 찾게되면 이벤트를 수신한다
BubbleUp : 이벤트를 부모 엘리먼트에 전파한다. BubbleUp이 생략되어 전파되지 않는 이벤트도 존재함
```



### (1) Propagation path

- TrickleDown 

  - 이벤트의 시작 단계로 대상을 탐색하여 마우스 입력이나 키보드 입력 등으로 발생한 이벤트를 전달한다
  - 대상의 선택은 이벤트마다 다르다. 예를들면 
    - 마우스 클릭의 대상은 마우스 포지션 아래에 위치한 요소
    - 키보드 입력의 대상은 현재 포커스가 있는 요소

- Target

  - 이벤트를 전달받고 처리하는 단계

  - Target에 등록된 콜백을 처리하고 추가로 [ExecuteDefaultActionAtTarget()](https://docs.unity3d.com/2022.1/Documentation/ScriptReference/UIElements.CallbackEventHandler.ExecuteDefaultActionAtTarget.html) 이벤트 함수가 실행된다.
    - 타겟의 콜백작업 후 버블업 전에 호출되므로 필요한 경우 오버라이딩해서 사용하자

- BubbleUp

  - Target에 전달된 이벤트를 부모 엘리먼트로 전달하는 단계로 루트까지 등록된 콜백이 실행됨
  - 버블업이 생략되는 이벤트도 존재함
  - 모든 콜백이 처리되고 나면 [ExecuteDefaultAction()](https://docs.unity3d.com/2022.2/Documentation/ScriptReference/UIElements.CallbackEventHandler.ExecuteDefaultAction.html) 이벤트 함수가 실행된다.
    - 버블업 이후 부모 요소의 모든 콜백 이벤트가 마무리된 후 호출되므로 필요한 경우 오버라이딩해서 사용하자



### (2) Event Callback

- 엘리먼트에 Event에 대한 콜백을 등록하면 이벤트 발생시 등록된 콜백이 호출된다
- 기본적으로 등록된 콜백은 Target단계에서 대상의 콜백이 실행되고 그 후 버블업 단계에서 상위요소에 등록된 콜백이 순차적으로 실행된다



##### 가. TrickleDown

- 필요에 따라 부모요소가 자식 요소보다 먼저 반응하도록 하려면 콜백을 등록할때 TrickleDown 옵션을 지정하여 버블업 단계가 아닌 TriclkeDown 단계에서 콜백을 호출하도록 할수 있다

![image-20230120103631462](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230120103631462.png)

```
// Register a callback for the trickle-down phase
myElement.RegisterCallback<MouseDownEvent>(MyCallback, TrickleDown.TrickleDown);

NoTriclkeDown : 버블업 단계에서 실행
TriclkeDown : TriclkeDown 단계에서 실행
```



##### 나. Custom Param

- 필요에 따라 콜백 함수에 커스텀 파라미터를 등록할 수 있다

```
// Send user data along to the callback
myElement.RegisterCallback<MouseDownEvent, MyType>(MyCallbackWithData, myData);

void MyCallbackWithData(MouseDownEvent evt, MyType data) { /* ... */ }
```



### (3) Picking Mode

- Visual Element의 마우스 이벤트를 제어하는 설정으로 Position과 Ignore가 있다
  - Position : 마우스 이벤트 수신
  - Ignore : 마우스 이벤트 무시
- 해당 옵션은 UI Builder를 통해서도 설정이 가능하다



### (4) FocusRing

- 엘리먼트의 포커스 순서는 아래와 같이 깊이탐색으로 정해진다.
- tabIndex를 설정해 필요에 따라 순서를 변경할 수 있다

![](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/focus-order.png)

```
VisualTree를 깊이 탐색하여 대상을 선택한다
위 트리의 루트를 기준으로 순서는 F, B, A, D, C, E, G, I, H가 된다
```



## Manipulator

- 콜백 만으로 이벤트를 처리하려면 불편한 점들이 있다
- 마우스를 통해 엘리먼트를 드래그 하여 움직이는 이벤트를 예로보면
  - MouseDown & Start Move -> Move & Drag -> MouseUp & End Move와 같이 다수의 이벤트를 유기적으로 처리할 필요가 있다
  - 또한 이런 이벤트를 매번 필요한 엘리먼트 마다 콜백을 등록해서 만드는 것은 상당히 번거롭다
- 이러한 불편사항을 해소하기 위해 유니티에서는 Manipulator를 제공한다



### (1) Custom Manipulator 만들기

- Manipulator를 만들기 위해서는 Manipulator 클래스를 상속하고 원하는 이벤트에 커스텀한 콜백함수를 등록하면 된다
  - 아래는 유니티에서 제공하는 Manipulator 클래스의 종류이다
  - 편의를 위해 자주 사용하는 마우스나 키보드 이벤트 등의 Manipulator를 제공하고, 필요하다면 디폴트 Manipulator를 이용해 처음부터 원하는 형태로 제작하는 것도 가능하다

![image-20230120133300861](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230120133300861.png) 



### (2) Example

- 아래는 MouseUp과 Down 두개의 이벤트를 하나의 Manipulator로 묶고 필요한 요소에 해당 이벤트를 등록하는 예이다
  - 두 개의 이벤트를 하나의 독립적인 Manipulator로 만들어 제공
  - 해당 이벤트가 필요한 엘리먼트에 Manipulator 추가

```
//서로 다른 두개의 엘리먼트 생성
VisualElement newButton = new Button();
VisualElement newElement = new VisualElement();

//각각에 MouseEvent Manipulator 등록
newButton.AddManipulator(new MouseEventLogger());
newElement.AddManipulator(new MouseEventLogger());

//MouseUp, Down Event에 대한 Log를 출력하는 Manipulator
class MouseEventLogger : Manipulator
    {
        protected override void RegisterCallbacksOnTarget()
        {
            target.RegisterCallback<MouseUpEvent>(OnMouseUpEvent);
            target.RegisterCallback<MouseDownEvent>(OnMouseDownEvent);
        }

        protected override void UnregisterCallbacksFromTarget()
        {
            target.UnregisterCallback<MouseUpEvent>(OnMouseUpEvent);
            target.UnregisterCallback<MouseDownEvent>(OnMouseDownEvent);
        }

        void OnMouseUpEvent(MouseEventBase<MouseUpEvent> evt)
        {
            Debug.Log("Mouse Up " + evt + " in " + evt.propagationPhase + " for target " + evt.target);
        }

        void OnMouseDownEvent(MouseEventBase<MouseDownEvent> evt)
        {
            Debug.Log("Mouse Down " + evt + " in " + evt.propagationPhase + " for target " + evt.target);
        }
    }
```



## Event Reference

- 이벤트 목록과 정보는 [공식 문서](https://docs.unity.cn/Manual/UIE-Events-Reference.html)에 카테고리 별로 자세히 정리되어 있다
- 버블업이 생략되는 이벤트나 파라미터 등을 확인할 수 있으니 필요하면 공식 문서를 참고하자

![image-20230120105829032](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230120105829032.png)

![image-20230120105806206](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230120105806206.png)



## Stop event propagation and cancel default actions

- 필요에 따라 Propagation 단계에서 호출되는 Default Action이나 버블업 단계를 막아야 하는 경우가 발생한다
- 엘리먼트의 이벤트 핸들러나 ExecuteDefaultActionAtTarget 함수를 오버라이딩 하고 StopPropagation()이나, PreventDefaultAction() 함수를 호출하여 버블업이나 DefaultAction을 취소 처리하는것이 가능하다
  - StopPropagation : 버블업 취소
  - PreventDefaultAction : ExecuteDefaultActionAtTarget()나 ExecuteDefaultAction() 취소
- 아래는 작업 중 발생한 예이다

#### [BubbleUp Issue]

![bubbleup](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/bubbleup.gif)

```
부모인 Node 엘리먼트와 자식인 ListView 엘리먼트는 각각 엘리먼트에 맞는 마우스 이벤트를 가지고 있다
문제는 ListView 이벤트에서 처리될 마우스 이벤트가 버블업 단계로 넘어가며 상위인 노드에 전달되어 의도와 다른 동작을 하는 문제가 발생한다
```



#### [Fix]

- 버블업 취소 후 리스트뷰 내의 이벤트는 더 이상 상위 노드로 전달되지 않는다

![bubbleup2](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/bubbleup2.gif)

```
protected override void ExecuteDefaultActionAtTarget(EventBase evt)
{
	base.ExecuteDefaultActionAtTarget(evt);

    //버블업 취소
    evt.StopPropagation();
}

버블업으로 인한 문제이므로 ListView를 확장하고 ExecuteDefaultActionAtTarget 이벤트 함수를 오버라이딩한 후 수신되는 이벤트에 StopPropagation 함수를 호출하여 해당 컨트롤 내에서 발생한 이벤트에 대한 버블업을 취소한다
```



# Ref

- [Dispatching Event](https://docs.unity.cn/Manual/UIE-Events-Reference.html)

- [Event Process](https://docs.unity.cn/Manual/UIE-Events-Handling.html)
- [Event Reference](https://docs.unity.cn/Manual/UIE-Events-Reference.html)
- [https://www.fast-system.jp/unity-ui-elements-samples/](https://www.fast-system.jp/unity-ui-elements-samples/)