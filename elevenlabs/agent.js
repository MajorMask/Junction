import { useConversation } from "@elevenlabs/react";

const conversation = useConversation({
  agentId: "3aa3bbb6a54c44bc160ea0ebc45aa0c1b72b1f13903bea3e86bd64e2a928eb2e",
});

// Start conversation
conversation.startSession();
