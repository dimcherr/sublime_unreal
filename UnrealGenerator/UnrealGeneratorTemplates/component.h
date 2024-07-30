#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "{name}.generated.h"

UCLASS(BlueprintType, Blueprintable)
class {projectname}_API U{name} : public UActorComponent
{{
	GENERATED_BODY()

public:	
	U{name}();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
}};