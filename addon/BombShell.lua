frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:ClearAllPoints()
frame:SetHeight(600)
frame:SetWidth(320)

-- HELPER FUNCTIONS --

function starts_with(str, start)
   return str:sub(1, #start) == start
end

function split(s, delimiter)
    result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end

function replace_char(pos, str, r)
    return str:sub(1, pos-1) .. r .. str:sub(pos+1)
end

-- END OF HELPER FUNCTIONS --

function SetPlayerState(attr, val)
    local current = frame.playerState:GetText()

    if (not current) then
        current = string.rep("0", table.getn(PLAYER_STATE))
    end

    frame.playerState:SetText(replace_char(PLAYER_STATE[attr], current,val))
    end

function SetTargetState(attr, val)
    local current = frame.targetState:GetText()

    if (not current) then
        current = string.rep("0", table.getn(TARGET_STATE))
    end

    frame.targetState:SetText(replace_char(TARGET_STATE[attr], current, val))
end

function SetTargetGuid()
    local guid = UnitGUID("target")
    local target = GetTargetHealth()
    if not guid or target == -1 then
        guid = "-1"
    end
    guid = split(guid, "-")

    frame.targetId:SetText(guid[6] .. guid[7])
end

PARENT = "GameFontNormal"
FONT = "Interface\\AddOns\\BombShell\\data\\font\\default.ttf"
FONT_SIZE = 32
START = 80
LINE_SPACE = 40
DATA = {"text", "mana", "posx", "posy", "facing", "playerState", "targetHealth", "targetState", "targetId" }
PLAYER_STATE = {combat=1, casting=2, last_ability=3, inventory=4, hasPet=5, firstResource=6}
TARGET_STATE = {distance=1}

for k, v in ipairs(DATA) do
    local t = frame:CreateFontString(v, "BACKGROUND", PARENT)
    t:SetPoint("CENTER", 0, START - k * LINE_SPACE)
    t:SetJustifyH("LEFT")
    t:SetTextColor(0, 0, 0, 1)
    t:SetFont(FONT, FONT_SIZE)
    frame[v] = t
end

function GetPlayerHealth()
    local max = UnitHealthMax("player")
    local perc = floor(UnitHealth("player") / max * 100)

    return perc
end

function GetPlayerMana()
    local max = UnitPowerMax("player")
    local perc = floor(UnitPower("player") / max * 100)

    return perc
end

function GetTargetHealth()
    local max = UnitHealthMax("target")
    if max == 0 then
        return -1
    end
    local perc = floor(UnitHealth("target") / max * 100)

    return perc
end

function GetTargetDistance()
    local distance = 0
    if (CheckInteractDistance("target", 3)) then
                distance = 1
            elseif (CheckInteractDistance("target", 4)) then
                distance = 2
    end

    return distance
end

function GetSpellState()
    local info = {CombatLogGetCurrentEventInfo()}
            --DEFAULT_CHAT_FRAME:AddMessage("COMBAT LOG " .. info[2] .. " " .. info[4] .. " " ..info[15] )
    if (info[2] == 'SPELL_CAST_FAILED' and starts_with(info[4], 'Player')) then
        if (info[15] == "SPELL_FAILED_TOO_CLOSE") then
            return 3
        elseif (info[15] == "Target not in line of sight") then
            return 2
        elseif (info[15] == "Out of range") then
            return 1
        elseif (info[15] == "SPELL_FAILED_NOT_BEHIND") then
            return 4
        elseif (info[15] == "Target needs to be in front of you") then
            return 5
        elseif (info[15] == "SPELL_FAILED_BAD_IMPLICIT_TARGETS") then
            return 6
        end

    end

    return 0
end

function IsFirstClassResourceAvailable()
    local soulShards = GetItemCount("Soul Shard")
    local available = 0

    if soulShards > 0 then
        available = 1
    end

    return available
end

function GetPlayerCastingState()
    local spell, _, _, _, _, endTime = CastingInfo()
    local ret = 0
    if spell then
        ret = 1
    end

    return ret
end

function IsPetExist()
    local petSpells, _ = HasPetSpells()

    if petSpells == nil then
        return 0
    end

    return 1

end

function GetFacing()
    return GetPlayerFacing()
end

function IsInventoryFull()
    local freeSlots = 0
    for bagId=0,4 do
        numSlots, bagType = GetContainerNumFreeSlots(bagId)
        if bagType == 0 then
            freeSlots = freeSlots + numSlots
        end
    end

    local isFull = 0

    if freeSlots == 0 then
        isFull = 1
    end

    return isFull
end

function GetTruePosition()
    local mapID = C_Map.GetBestMapForUnit("player")
    local map = WorldMapFrame.ScrollContainer
    local width = map:GetWidth()
    local height = map:GetHeight()

	if mapID then
		local mapPos = C_Map.GetPlayerMapPosition(mapID, "player")
        if mapPos then
            local x, y = mapPos:GetXY()
            return x * width, y * height
        end
		end

    return -1, -1
end

frame:SetPoint("LEFT", 0, 200)

frame:SetBackdrop(
    {
        insets = {left = 4, right = 4, top = 4, bottom = 4},
        backdropColor = {r = 1, g = 1, b = 1, a = 0}
    }
)
frame.texture = frame:CreateTexture(nil, "BACKGROUND")
frame.texture:SetAllPoints(true)
frame.texture:SetColorTexture(1, 1, 1, 1)

DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
frame:RegisterEvent("UNIT_HEALTH")
frame:RegisterEvent("UNIT_POWER_UPDATE")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")
frame:RegisterEvent("PLAYER_REGEN_ENABLED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
frame:RegisterEvent("LOOT_CLOSED")
frame:RegisterEvent("UNIT_PET")

frame:SetScript(
    "OnEvent",
    function(self, event, ...)
        if (event == "PLAYER_ENTERING_WORLD") then
            DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
            frame.text:SetText("" .. GetPlayerHealth())
            frame.mana:SetText("" .. GetPlayerMana())
            SetPlayerState("combat", "0")
            SetPlayerState("last_ability", "0")
            SetTargetState("distance", "0")
            SetPlayerState("inventory",  IsInventoryFull())
            SetPlayerState("hasPet",  IsPetExist())
            SetPlayerState("firstResource", IsFirstClassResourceAvailable())
            frame.targetHealth:SetText("" .. -1)
            frame.targetId:SetText("-1")
        elseif (event == "UNIT_HEALTH") then
            local health = GetPlayerHealth()
            local targetHealth = GetTargetHealth()
            frame.text:SetText("" .. health)
            frame.targetHealth:SetText("" .. targetHealth)
        elseif (event == "UNIT_POWER_UPDATE") then
            local mana = GetPlayerMana()
            frame.mana:SetText("" .. mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            SetPlayerState("combat", "0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            SetPlayerState("combat", "1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local tuid = UnitLevel("target")
            local targetHealth = GetTargetHealth()
            local distance = GetTargetDistance()
            SetTargetState("distance", distance)
            frame.targetHealth:SetText("" .. targetHealth)
            if targetHealth == -1 then
                frame.targetId:SetText("-1")
            else
                SetTargetGuid()
            end
        elseif (event == "COMBAT_LOG_EVENT_UNFILTERED") then
            SetPlayerState("last_ability",  GetSpellState())
        elseif (event == "LOOT_CLOSED") then
            SetPlayerState("inventory",  IsInventoryFull())
        elseif (event == "UNIT_PET") then
            SetPlayerState("hasPet",  IsPetExist())
        end
    end
)

frame:SetScript(
    "OnUpdate",
    function(self, event)
        local posX, posY = GetTruePosition()
        local distance = GetTargetDistance()
        frame.posx:SetText("" .. string.sub(posX, 0, 8))
        frame.posy:SetText("" .. string.sub(posY, 0, 8))

        frame.facing:SetText("" .. string.sub(GetFacing(), 0, 8))

        SetPlayerState("casting", GetPlayerCastingState())
        SetTargetState("distance", distance)
        SetPlayerState("firstResource", IsFirstClassResourceAvailable())
    end
)

frame:Show()
