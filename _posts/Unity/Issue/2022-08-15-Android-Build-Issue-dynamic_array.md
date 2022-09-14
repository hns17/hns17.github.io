---
title: "Unity Android Build Issue ~dynamic_array"
categories: [Unity/Issue]
tag : ["Unity", "Android_Build_Issue"]
---



# Unity 2021 Android Build Issue

- Unity Version : 2021.3
- Build Platform : Android

- Project를 2020에서 2021로 변경 후 빌드시 아래와 같은 문제가 발생
- ![image-20220814220000897](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220814220000897.png)

- ```
  Building Library\Bee\artifacts\Android\d8kzr\libil2cpp.so failed with output:
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `~dynamic_array':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\utils/dynamic_array.h:81:(.text._ZN6il2cpp5utils13dynamic_arrayIP11Il2CppClassLm8EED2Ev[_ZN6il2cpp5utils13dynamic_arrayIP11Il2CppClassLm8EED2Ev]+0x24): relocation truncated to fit: R_AARCH64_CALL26 against symbol `__clang_call_terminate' defined in .text.__clang_call_terminate[__clang_call_terminate] section in Library/Bee/artifacts/Android/d8kzr/jge3_bly-CSharp.o
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::FromGenericParameter(___Il2CppMetadataGenericParameterHandle const*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:286:(.text._ZN6il2cpp2vm5Class20FromGenericParameterEPK39___Il2CppMetadataGenericParameterHandle+0x284): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::Init(Il2CppClass*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:1589:(.text._ZN6il2cpp2vm5Class4InitEP11Il2CppClass+0xe8): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `Il2CppHashMap':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\PlaybackEngines\AndroidPlayer\NDK\toolchains\llvm\prebuilt\windows-x86_64\bin\..\sysroot\usr\include\c++\v1/vector:(.text._ZN13Il2CppHashMapIPK39___Il2CppMetadataGenericParameterHandleP11Il2CppClassN6il2cpp5utils15PassThroughHashIS2_EENSt6__ndk18equal_toIS2_EEN6google27libc_allocator_with_reallocINS9_4pairIK10KeyWrapperIS2_ES4_EEEEEC2EmRKS8_RKSB_[_ZN13Il2CppHashMapIPK39___Il2CppMetadataGenericParameterHandleP11Il2CppClassN6il2cpp5utils15PassThroughHashIS2_EENSt6__ndk18equal_toIS2_EEN6google27libc_allocator_with_reallocINS9_4pairIK10KeyWrapperIS2_ES4_EEEEEC2EmRKS8_RKSB_]+0x68): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `~FastAutoLock':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\utils\..\os/Mutex.h:86:(.text._ZN6il2cpp2os12FastAutoLockD2Ev[_ZN6il2cpp2os12FastAutoLockD2Ev]+0x50): relocation truncated to fit: R_AARCH64_CALL26 against symbol `__clang_call_terminate' defined in .text.__clang_call_terminate[__clang_call_terminate] section in Library/Bee/artifacts/Android/d8kzr/jge3_bly-CSharp.o
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::SetupEvents(Il2CppClass*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:1393:(.text._ZN6il2cpp2vm5Class11SetupEventsEP11Il2CppClass+0xf0): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::SetupFields(Il2CppClass*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:1112:(.text._ZN6il2cpp2vm5Class11SetupFieldsEP11Il2CppClass+0xe8): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::GetFieldFromName(Il2CppClass*, char const*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:362:(.text._ZN6il2cpp2vm5Class16GetFieldFromNameEP11Il2CppClassPKc+0x3c): relocation truncated to fit: R_AARCH64_CALL26 against symbol `strcmp@@LIBC' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../sysroot/usr/lib/aarch64-linux-android/22/libc.so
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::SetupInterfaces(Il2CppClass*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:1480:(.text._ZN6il2cpp2vm5Class15SetupInterfacesEP11Il2CppClass+0xe8): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::SetupMethods(Il2CppClass*)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:1211:(.text._ZN6il2cpp2vm5Class12SetupMethodsEP11Il2CppClass+0xf0): relocation truncated to fit: R_AARCH64_CALL26 against symbol `_Unwind_Resume' defined in .text section in C:/Program Files/Unity/Hub/Editor/2021.3.8f1/Editor/Data/PlaybackEngines/AndroidPlayer/NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/../lib/gcc/aarch64-linux-android/4.9.x\libgcc_real.a(unwind-dw2.o)
  Library/Bee/artifacts/Android/87lik/17fa_u_vm6.lump.o: In function `il2cpp::vm::Class::GetMethodFromNameFlagsAndSig(Il2CppClass*, char const*, int, int, Il2CppType const**)':
  C:/Program Files\Unity\Hub\Editor\2021.3.8f1\Editor\Data\il2cpp\libil2cpp\vm/Class.cpp:468:(.text._ZN6il2cpp2vm5Class28GetMethodFromNameFlagsAndSigEP11Il2CppClassPKciiPPK10Il2CppType+0x9c): additional relocation overflows omitted from the output
  clang++: error: linker command failed with exit code 1 (use -v to see invocation)
  UnityEngine.GUIUtility:ProcessEvent (int,intptr,bool&)
  
  ```

- 구글링 한 결과 빌드시 스크립트 디버깅을 활성화하면 Android NDK에서 문제가 발생한다는 내용을 확인함.



# 해결방법

-  IL2CPP 코드 생성을 더 빠른(작은)빌드로 변형 후 빌드하기
- ![image-20220814220535257](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220814220535257.png)



# Ref

[https://forum.unity.com/threads/im-able-to-build-both-production-and-development-but-not-script-debugging-on.1187170/](https://forum.unity.com/threads/im-able-to-build-both-production-and-development-but-not-script-debugging-on.1187170/)