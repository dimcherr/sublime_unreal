#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "{name}.generated.h"

UCLASS()
class {projectname}_API A{name} : public AActor
{{
	GENERATED_BODY()

public:

	A{name}();	

	virtual void Tick(float DeltaTime) override;

protected:
	virtual void BeginPlay() override;

private:

}};