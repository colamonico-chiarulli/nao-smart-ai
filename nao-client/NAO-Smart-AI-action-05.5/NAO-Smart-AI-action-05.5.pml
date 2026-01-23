<?xml version="1.0" encoding="UTF-8" ?>
<Package name="NAO-Smart-AI-action-05.5" format_version="5">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="behavior_1" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs>
        <Dialog name="smart_ai_offline" src="smart_ai_offline/smart_ai_offline.dlg" />
        <Dialog name="smart_ai_online" src="smart_ai_online/smart_ai_online.dlg" />
    </Dialogs>
    <Resources>
        <File name="mikhael-landscape-paisaje" src="behavior_1/sounds/mikhael-landscape-paisaje.ogg" />
        <File name="camera1" src="behavior_1/sounds/camera1.ogg" />
        <File name="epicsax" src="behavior_1/sounds/epicsax.ogg" />
        <File name="court-boom" src="behavior_1/sounds/court-boom.wav" />
        <File name="smoke on the water" src="behavior_1/sounds/smoke on the water.ogg" />
        <File name="camera1" src="behavior_1/camera1.ogg" />
        <File name="Macarena-dance2" src="behavior_1/sounds/Macarena-dance.ogg" />
        <File name="evolution_of_dance_SHORT" src="behavior_1/sounds/evolution_of_dance_SHORT.mp3" />
    </Resources>
    <Topics>
        <Topic name="smart_ai_offline_iti" src="smart_ai_offline/smart_ai_offline_iti.top" topicName="smart_ai_offline" language="it_IT" nuance="iti" />
        <Topic name="smart_ai_offline_enu" src="smart_ai_offline/smart_ai_offline_enu.top" topicName="smart_ai_offline" language="en_US" nuance="enu" />
        <Topic name="smart_ai_online_enu" src="smart_ai_online/smart_ai_online_enu.top" topicName="smart_ai_online" language="en_US" nuance="enu" />
        <Topic name="smart_ai_online_iti" src="smart_ai_online/smart_ai_online_iti.top" topicName="smart_ai_online" language="it_IT" nuance="iti" />
    </Topics>
    <IgnoredPaths />
    <Translations auto-fill="it_IT">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
        <Translation name="translation_it_IT" src="translations/translation_it_IT.ts" language="it_IT" />
    </Translations>
</Package>
