#include "{includename}.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputMappingContext.h"
#include "InputAction.h"

A{name}::A{name}()
{{
	PrimaryActorTick.bCanEverTick = true;
}}

void A{name}::BeginPlay()
{{
	Super::BeginPlay();
}}

void A{name}::Tick(float DeltaTime)
{{
	Super::Tick(DeltaTime);
}}

void A{name}::SetupInputComponent()
{{
	Super::SetupInputComponent();
	SetupInputMapping();

	UEnhancedInputComponent* Input = Cast<UEnhancedInputComponent>(InputComponent);
	MyCharacter = Cast<ACharacterAnastasia>(GetCharacter());
	if (MyCharacter != nullptr)
	{
		// TODO Setup input
	}
}}

void A{name}::SetupInputMapping()
{{
	if (ULocalPlayer* LocalPlayer = Cast<ULocalPlayer>(Player))
	{
		if (UEnhancedInputLocalPlayerSubsystem* InputSystem = LocalPlayer->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
		{
			if (!InputMapping.IsNull())
			{
				int32 Priority = 0;
				InputSystem->AddMappingContext(InputMapping.LoadSynchronous(), Priority);
			}
		}
	}
}}
