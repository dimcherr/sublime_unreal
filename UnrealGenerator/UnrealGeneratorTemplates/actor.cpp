#include "{includename}.h"

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
