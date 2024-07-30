#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "{name}.generated.h"

UCLASS()
class {projectname}_API A{name} : public APlayerController
{{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere, Category="Input")
	TSoftObjectPtr<class UInputMappingContext> InputMapping;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	class AMyCharacter* MyCharacter;

	A{name}();	

protected:
	virtual void BeginPlay() override;
	virtual void SetupInputComponent() override;

public:	
	virtual void Tick(float DeltaTime) override;

private:
	UFUNCTION()
	void SetupInputMapping();
}};