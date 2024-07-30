#include "{includename}.h"

U{name}::U{name}()
{{
	PrimaryComponentTick.bCanEverTick = true;
}}

void U{name}::BeginPlay()
{{
	Super::BeginPlay();
}}

void U{name}::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}}