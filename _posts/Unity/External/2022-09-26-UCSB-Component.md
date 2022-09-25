---
title: "UnityChanSpringBone(UCSB) Component Manual"
categories: [Unity/External(Asset/Lib/Etc)]
tag : ["Unity", "UCSB", "SpringBone", "UnityChanSpringBone", "UCSB Component", "Manual"]
---



# UCSB 컴포넌트 매뉴얼

- UnityChanSpringBone 패키지에서 제공하는 컴포넌트들 정리
- UnityChan에 포함된 일본어 매뉴얼을 기반으로 작성



## 1. SpringBone Window

```
스프링본 윈도우는 셋업을 위한 편의 기능을 제공합니다.
Spring Manager 컴포넌트의 '스프링 윈도우 열기' 버튼 또는 메뉴 [Window-Animation-SpringBone]을 통해 열수 있습니다.
```

![image-20220925233246315](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925233246315.png)



#### (1) Show

![image-20220925233659037](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925233659037.png)

- 선택된 본만 표시
  - 선택된 SpringBone만 gizmo가 표시됩니다.
  - Spring Bone이 많으면 gizmo의 표시가 무거워져 정보량이 많아지므로 선택된 것만 표시하면 파악하기 쉽습니다.

- 선택된 콜라이더만 표시
  - 선택된 콜라이더의 gizmo만 표시됩니다.

- 본의 콜라이더을 표시
  - Spring Bone의 콜라이더(Sphere)를 표시합니다.

- 본 이름 표시
  - Scene뷰에 본 이름을 표시.
  - 이쪽도 Spring Bone이 많으면 무거워지므로 필요할 때 이외에는 숨기는 것을 권장합니다.



#### (2) Dynamic CSV

```
다이내믹스 CSV의 읽기와 저장 기능.
```

- 불러오기

  - CSV를 읽어들여 캐릭터의 다이나믹 정보를 셋업합니다.

- 저장하기
  캐릭터의 다이나믹 정보를 CSV에 저장합니다.

  

#### (3) 스프링본

![image-20220925234232138](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925234232138.png)

- 스프링본 추가
  - 선택된 오브젝트 Spring Bone 컴포넌트를 추가합니다.
  - Spring Bone 컴포넌트를 추가할 오브젝트에는 자식 오브젝트가 필요하기 때문에 자식이 없는 객체에는 추가되지 않습니다.
    - 추가하고자 하는 지글본이 최하단일 경우 해당 본에 빈 자식 오브젝트를 추가하면 SpringBone 컴포넌트를 이용할 수 있다.

- Pivot 설정
  - 선택된 SpringBone의 Pivot 오브젝트를 생성합니다.
  - Pivot 오브젝트는 SpringBonePivot 컴포넌트를 가지며, Spring Bone과 같은 계층(Spring Bone 부모의 자녀)에 배치됩니다.
    - Pivot을 설정하지 않는 경우 SpringBone의 기본 Pivot은 부모 오브젝트로 설정됩니다.

- 매니저 생성 및 업데이트
  - 선택된 오브젝트에 Spring Manager가 없는 경우 Spring Manager를 추가하고, 해당 객체 이하의 Spring Bone을 검출하여 Spring Manager에 다시 등록합니다.

- 스프링본을 미러
  - Spring Bone 정보를 선택된 기준(좌/우)에서 그 반대로 반전하기 위한 '스프링본을 미러' 창을 표시합니다.(후술)

- 본과 자식 본 선택
  - 선택된 오브젝트 이하의 Spring Bone을 모두 선택.
- 선택된 스프링본 삭제
  - 선택된 오브젝트의 스프링본 컴포넌트 제거

- 선택된 본 및 자식 본 본 삭제
  - 선택된 오브젝트 이하의 전체 Spring Bone과 Spring Manager를 삭제합니다.



#### (4) 콜라이더

![image-20220925235717885](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925235717885.png)

- Sphere
  - 신규 Sphere 콜라이더(SpringSphere Collider)를 선택된 오브젝트의 자식으로 생성.

- Capsule
  - 신규 Capsule콜라이더(SpringCapsuleCollider)를 선택된 오브젝트의 자식으로 생성.
  - 생성시에 대상 본에 자식 오브젝트가 있는 경우, 그 본과 자식의 위치에 맞춰 배치됩니다.

- Panel
  - 신규 Panel콜라이더(SpringPanelCollider)를 선택된 오브젝트의 자식으로 생성.

- 캡슐의 위치를 부모로
  - 선택된 캡슐의 부모 중 다른 자식 오브젝트가 있는 경우 해당 캡슐의 위치를 그 부모와 자식 기준으로 맞춥니다.
  - 새로 작성할 때와 동일하게 배치됩니다.

- 스프링본에서 콜라이더를 제외거
  - 선택된 Spring Bone 컴포넌트에 등록된 모든 콜라이더를 제거합니다.

- 대상 및 자식 콜라이더 삭제
  - 선택된 오브젝트 및 자식 계층의 콜라이더를 모두 삭제합니다.

- CleanUp

  - 어떤 Spring Bone에도 등록되어 있지 않은 콜라이더를 삭제합니다.

  - 또한 전체 Spring Bone 컴포넌트의 콜라이더 목록에 None이 있다면 목록에서 제거합니다.

    

## 2. SpringManager

```
다이나믹 처리를 위한 메인 컴포넌트
하나의 캐릭터에 하나의 루트 오브젝트만 사용
계층구조 상 다른 UCSB 컴포넌트보다 상위에 위치해야 함
```

![image-20220925111533255](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925111533255.png)

#### (1) Button

![image-20220925113519695](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925113519695.png)

- 스프링 윈도우 열기
- 스프링 본 전체 선택
  - SpringBone Component가 설치된 자식 오브젝트 전부 선택
- 스프링본 리스트 업데이트 : 매니저에서 누락된 스프링본 컴포넌트 정보 전부 찾아서 추가
  - 스크립트 또는 인스펙터를 통해 스프링본 컴포넌트를 추가할 경우 업데이트 하지 않으면 매니저에 추가되지 않음



#### (2) properties

![image-20220925113549338](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925113549338.png)

- Automatic Update(자동 갱신) 

  - (프로그래머용) 자동 갱신을 유효하게 합니다. 처음에는 켜져 있는데 스크립트 측에서 다이내믹스 처리 타이밍을 컨트롤 할 때는 체크를 제거하고, SpringManager의 Update Dynamics() 메서드를 수동으로 호출할 수 있습니다.

- IsPaused (일시정지)

  - 다이내믹스 처리 일시 정지. 게임을 일시 정지시킬 때는 이쪽의 체크도 넣으면 일시 정지 중에 다이내믹스는 움직이지 않습니다.

  - 모션 외의 작용 Off(ucsb에서 계산하는 2차적인 가속도 바람 같은 것들)

  Simulation Frame Rate (처리 빈도)
  다이내믹스 처리 간격을 제어합니다.고정 수치로 하면 다이내믹스의 거동이 안정됩니다.

  - 1로 하면 Time.delta Time과 같은 간격으로 움직이지만 프레임 레이트가 변동되면 다소 날뛰게 될 가능성이 있습니다.
  안정을 위해 60으로 설정하는 것이 좋습니다.


- Dynamic Ratio(다이나믹스 비율)[실험 중]
  - (프로그래머용) 모션과 다이내믹스를 블렌딩하는 비율. 
  - 단, 모션으로 흔들림 본의 모션을 붙이는 경우는 평소 없기 때문에 Spring Manager의 Update Bone Is Animated States () 메서드에서 어떤 흔들림 본이 모션으로 움직일지를 그 모션의 재생시 등에 지정해야 합니다.

- Gravity (중력)
  - 전체에 가하는 중력 파라미터. 각 SpringBone의 중력 파라미터에 추가됩니다.

- Bounce (튀김)[실험 중]
  - 콜리젼에 맞았을 때의 뛰는 비율. (현재 실험 단계에서 본래 각 본에 붙이는 파라미터가 될 예정입니다.)
- Friction (마찰)[실험 중]
  충돌시 마찰 비율. (현재 실험 단계에서 본래 각 본에 붙이는 파라미터가 될 예정입니다.)



#### (3) Constraints(제한 기능)

![image-20220925114719430](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925114719430.png)

- Enable Angle Limits
  - 각도 제한 활성화

- Enable Collision
  - 콜라이더 활성화

- Enable Length Limits
  - 거리 제한 활성화

※ SpringBone Component에서 설정한 제한 기능을 일괄적으로 On/Off할 때 사용



#### (4) Ground Collision

![image-20220925115608913](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925115608913.png)

- Collide With Ground
  - UCSB용 지면 충돌 판정 활성화

- Ground Height
  - 지면 높이(Y 좌표)

```
지면의 판정은 지정한 높이(GroundHeight)의 평면이 됩니다.
Scene뷰의 Gizmo에서 발밑의 사각 테두리로 표시됩니다.
현재는 대각선이나 세로로 사용이 불가능합니다.
대상의 위치가 GroundHeigt 보다 아래로 내려가면 다이나믹 움직임도 낙하 상태처럼 변화함
```



#### (5) Bones

![image-20220925121351225](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925121351225.png)

- Spring Bones
  - 등록된 Spring Bone 목록. 
  - Spring Bone Window나 SpringBoneListUpdate버튼을 쓰다 보면 평소에 이걸 직접 손으로 만질 필요는 없음



#### (6) Gizmo

![image-20220925121537106](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925121537106.png)

- Bone Color (본 색)
  - SpringBone이 표시되는 색상.

- Collision Color (충돌체 판정의 색상)
  - 충돌체 판정(구체, 캡슐, 판)이 표시되는 색상

- Ground Collision Color (땅바닥에 닿는 판정 색상)
  - 지면 판정이 표시되는 색상.

- Angle Limit Draw Scale (각도 제한의 묘화 확대율)
  - 각도 제한 축이 표시되는 크기.

※ 각 요소의 Gizmo 및 Handle 색상과 각도 제한 크기를 지정합니다.에디터에서만 사용됩니다.



## 3. SpringBone

![image-20220925121920805](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925121920805.png)

#### (1) Button & Toggle

![image-20220925191802241](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925191802241.png)

- Pivot 선택 Button
  - SpringBone의 Pivot으로 지정된 객체 선택
- 매니저(읽기 전용)
  - 이 Spring Bone이 등록된 Spring Manager를 나타냅니다.
- Enable
  - 이 본의 다이내믹스 On/Off



#### (2) 힘

![image-20220925191819330](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925191819330.png)

- 경도
  - 본의 경도. 높을수록 초기 위치로 돌아가려는 힘이 강함.
  - 낮으면 부드러운 흔들림이 되어 중력 등에 상태가 쉽게 변함
  - 특별히 정해진 상한은 없지만 Inspector에서는 슬라이더는 5000에서 멈춥니다.
- 공기 저항
  - 공기저항에 해당하는 값. 강하면 강할수록 움직임이 느려집니다.
  - 반대로 낮으면 스프링처럼 빠른 움직임이 됩니다.
  - '감쇠력'이라고도 할 수 있습니다.
  - 이 파라미터는 0~1의 폭이 됩니다.

-  중력
  - Y축에 마이너스 수치를 넣으면 그 본 특유의 중력이 됩니다.
  - 플러스 Y 하면 반대로 떠요.'이 뼈는 더 중력을 내고 싶다.'라고 할 때 사용합니다.
- 바람의 영향값
  - 바람의영향치.
  - 범위는 0~1이고, 0이면 영향을 받지 않으며 1이면 100% 영향을 받습니다.
  - 바람은 WindVolume Component에서 Control
  
  

#### (3) 각도제한

```
본이 움직일 수 있는 범위를 제한합니다.
본이 향하고 있는 방향 벡터는 X로 여겨지기 때문에, Y축과 Z축으로 각각의 각도 제한을 설정할 수 있습니다.

각도 제한은 'Pivot Object'라고 하는 객체의 방향(회전)에 대한 것입니다.

예를 들어 치마 본이 다리본보다 내려가지 않도록 하고 싶다면 각각의 치마의 Pivot 오브젝트를 다리본의 자식으로 만들면 됩니다.
(3D 툴에서 말하는 '페어런트 콘스트레인트'와 비슷한 것이라고 생각하셔도 됩니다만, 위치는 사용하지 않고 회전만을 기준으로 하고 있으며 이 Spring Bone 전용이므로 범용 페어런트 컨스트레인트는 되지 않습니다.)

설정 시 인스펙터 맨 아래에 각도 제한이 표시되며, Scene뷰에도 표시됩니다. Pivot Object를 돌리면 제한 방향을 확인할 수 있습니다.
```

![image-20220925191915471](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925191915471.png)



- Pivot
  - Pivot Object는 처음에는 그 Spring Bone의 부모로 설정되기 때문에 다른 오브젝트의 아이로 만들거나 방향을 바꾸거나 하려면 SpringBon 창에서 'Pivot 설정' 버튼을 눌러주세요.
  - 대상 Spring Bone에 대한 새로운 Spring Bone Pivot이라고 하는 컴포넌트가 있는 Game Object가 생성됩니다.
  - Spring Bone Pivot에 특별한 처리가 되어 있지 않지만, 다이내믹스 CSV에 저장되어 해당 CSV를 읽었을 때는 다시 작성하게 됩니다.

- 회전의 경도
  - 각도 제한이 유효한 경우, 본이 0도로 돌아가려는 힘입니다.
  - 격렬한 움직임으로 인해 본이 딱 상하한에 머무는 것이 아니라 더 천천히 멈추기 위한 수단입니다.
- 각 축(Y/Z)에 대한 제한
  - Y와 Z의 각 축의 각도 제한은 체크 박스에서 활성화, 각각의 「하한」과「상한」으로 조정할 수 있습니다.
    - 동시에 변경 : 활성화시 슬라이더가 동시에 움직입니다.
    - 하한으로 통일 : 상한선의 값을 하한선 값과 동일하게
    - 상한으로 통일 : 하한선의 값을 상한선의 값과 동일하게
    - 반전 : 상한선과 하한선의 값이 반전됩니다.



#### (4) 거리제한 [※ 실험 중]


![image-20220925193435685](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925193435685.png)

- 뼈가 거리를 유지하고자 하는 타겟을 지정합니다.
- 예를 들어 스커트의 본 사이의 거리가 너무 늘어나는 걸 해결하기위한  파라미터였지만, 현재는 제대로 작동하지 않으므로 사용하지 말 것을 권장합니다.



#### (5) 충돌판정

```
Spring Bone의 충돌 설정. 
각 Spring Bone은 Sphere 형태의 콜라이더를 가지며, UCSB의 콜라이더 컴포넌트와 상호작용 합니다.
UCSB 콜라이더 컴포넌트는 Sphere, Capsule, Panel 3 종류가 있습니다.
```

![image-20220925193652137](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925193652137.png)



- Radius
  - SpringBone 콜라이더의 Radius

- Sphere, Capsule, Panel
  - SpringBone 콜라이더와 상호작용할 UCSB 콜라이더  컴포넌트가 포함된 객체



#### (6) 각도제한 표시

```
Inspector 맨 아래에 각도 제한이 표시됩니다.
왼쪽은 Y축이고 오른쪽은 Z축.
색이 들어간 화살표는 하한과 상한을 나타냅니다.
회색 화살표(바로 아래)는 0도입니다.
재생 중에는 흰색 화살표가 본의 현재 방향을 나타냅니다.
```

![image-20220925194415015](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925194415015.png)

#### (7) 인스펙터 표시

```
만약을 위해 기존의 Inspector를 표시하기 위한 체크박스.
변수에 대한 정보를 에디터를 통한 커스텀 형태가 아닌 그대로 표시함
```

![image-20220925194544654](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925194544654.png)

## 4. Spring Collider

```
콜라이더는 SpringBoneWindow의 각 콜라이더 버튼으로 생성할 수 있습니다.
콜라이더는 Sphere, Capsule, Panel 세가지가 있습니다.
콜라이더는 선택된 오브젝트의 자식으로 생성됩니다.
또, 각 콜라이더에는 「Linked Renderer」라고 하는 파라미터가 있습니다.
이것이 지정되어 있는 경우는, 그 Renderer가 무효가 되어 있을 때, 콜라이더도 무효가 됩니다.
예를 들어, 모션에 의해 검 칼집이 숨겨지거나 하는 경우, 그 콜리젼을 동시에 무효화할 수 있습니다.
```



#### (1) Spring Sphere Collider

- 사용 예 : 머리, 허리 등
  - 앞머리, 뿌리머리 등은 콜라이더보다 각도 제한이 안정적입니다.

#### (2) Spring Capsule Collider

- 사용 예 : 팔, 다리, 몸통 등

#### (3) Spring Panel Collider

- 사용 예 : 긴 뒷머리, 포니테일, 망토 등이 등을 뚫고 들어가는 것을 막아줍니다.

- Panel는 가로와 세로 폭이 있고 자신의 Z축을 위의 법선 벡터라고 합니다.
- 충돌된 Spring Bone은 Panel의 뒤로 이동하지 않으며 반드시 Panel의 앞쪽(판의 로컬+Z)으로 움직입니다.

※ SpringCollider는 설치후 영향을 받을 SpringBone 컴포넌트의 충돌판정에 추가해야 반영됩니다. 



## 5. High Leg

```
치마 중간 본을 다리보다 내려가지 않도록 하고 싶지만, 가운데이기 때문에 좌우 어느 쪽도 되지 않을 때를 위한 컴포넌트입니다.
우선 Empty 오브젝트를 만들고 거기에 HighLeg 컴포넌트를 추가합니다.
High Leg에 허리와 양 다리 양쪽 끝의 본를 지정하고 허리보다 위로 올라가 있는 쪽 다리를 자신의 회전으로 합니다.
그것(혹은 그것의 어린이 객체)을 가운데 본의 Pivot으로 하면 어느 다리가 올라가 있어도 깨끗하게 피해줍니다.
```

![image-20220925220051981](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925220051981.png)

- HipPivot
  - 허리 본을 지정합니다.
- Legs
  - 다리본을 지정합니다. 각 다리의 부모(start)와 자녀(end)를 지정해야 합니다.



## 6. 외력

```
외부에서 Spring Bone에게 힘을 주는 것도 가능합니다.
장면 내 ForceProvider를 상속한 클래스는 설치된 각 Spring Bone에 힘을 줍니다.
독자적인 처리로 뭔가 힘을 주고 싶을 때는 ForceProvider를 상속받고 GetForceOnBone 메서드를 구현하십시오.

샘플에는 두 개의 클래스(ForceVolume, WindVolume)가 준비되어 있습니다.
```



#### (1) ForceVolume

```
고정된 힘을 전체 Spring Bone에게 줍니다.
힘의 방향은 추가되어 있는 transform의 방향입니다.
```

![image-20220925220545542](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925220545542.png)

- 강도 : 세기



#### (2) WindVolume

```
바람 같은 힘을 파도처럼 Spring Bone에게 줍니다.
Spring Bone 위치에 따라 영향이 변화합니다.
바람의 방향은 추가되어 있는 transform의 방향입니다.
실험중인 것으로 최적화 등은 되어 있지 않습니다.

또한 SpringBone의 "바람의 영향값" 파라미터는 여기서 사용됩니다.
영향치가 1일 경우에는 바람의영향을 100%받고 0일 경우에는 전혀 바람의 영향을 받지 않습니다.
```

![image-20220925221142037](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220925221142037.png)

- weight
  - 0 ~ 1 사이의 웨이트 값. 아래의 strength 파라미터에 곱셈됩니다.
- strength
  - 바람 전체의 세기
- amplitude
  - 바람이 방향을 향해 바깥쪽으로 퍼지는 거리.
- period
  - 현재 영향은 없지만 0으로 하면 바람이 움직이지 않게 됩니다.
- spin Period
  - 바람의 회전 간격을 지정합니다. 초 단위입니다. spinPeriod 간격으로 바람이 한 바퀴 회전합니다.
  - 회전중에 amplitude에 의해 바람이 퍼지는 방향이 바뀝니다(회전합니다).
- peak Distance
  - Spring Bone 위치에 따라 바람의 세기가 달라집니다.
  - 그 가장 강한 곳끼리의 거리를 지정합니다.
