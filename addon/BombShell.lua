local frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:ClearAllPoints()
frame:SetHeight(600)
frame:SetWidth(320)

PARENT = "GameFontNormal"
FONT = "Interface\\AddOns\\BombShell\\data\\font\\default.ttf"
FONT_SIZE = 24
START = 30
LINE_SPACE = 30
DATA = {"text", "mana", "posx", "posy", "targetHealth", "combat", "facing", "distance", "ability", "casting" }

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
    local max = UnitManaMax("player")
    local perc = floor(UnitMana("player") / max * 100)

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
    local timestamp, subevent, _ = CombatLogGetCurrentEventInfo()
            DEFAULT_CHAT_FRAME:AddMessage("COMBAT LOG " .. subevent .. timestamp)
            if (subevent == "SPELL_FAILED_TOO_CLOSE") then
                return 3
            elseif (subevent == "SPELL_FAILED_LINE_OF_SIGHT") then
                return 2
            elseif (subevent == "SPELL_FAILED_OUT_OF_RANGE") then
                return 1
            elseif (subevent == "SPELL_FAILED_NOT_BEHIND") then
                return 4
            elseif (subevent == "SPELL_FAILED_UNIT_NOT_INFRONT") then
                return 5
            elseif (subevent == "SPELL_FAILED_BAD_IMPLICIT_TARGETS") then
                return 6
            end
end

function GetPlayerCastingState()
    local spell, _, _, _, _, endTime = UnitCastingInfo("player")
    local ret = -1
    if spell then
        ret = endTime
    end

    return ret
end

function GetPlayerFacing()
    local p = Minimap
    local m = ({p:GetChildren()})[9]
    return m:GetFacing()
end

function GetTruePosition()
    local posX, posY = GetPlayerMapPosition("player")
    local w = WorldMapButton:GetWidth()
    local h = WorldMapButton:GetHeight()
    return posX * w, posY * h
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
frame.texture:SetTexture(1, 1, 1, 1)

frame:RegisterEvent("UNIT_HEALTH")
frame:RegisterEvent("UNIT_MANA")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")
frame:RegisterEvent("PLAYER_REGEN_ENABLED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")

frame:SetScript(
    "OnEvent",
    function(...)
        if (event == "PLAYER_ENTERING_WORLD") then
            SetMapToCurrentZone()
            DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
            frame.text:SetText("" .. GetPlayerHealth())
            frame.mana:SetText("" .. GetPlayerMana())
            frame.combat:SetText("0")
            frame.distance:SetText("" .. -1)
            frame.targetHealth:SetText("" .. -1)
--            frame.tuid:SetText("TID: " .. 0)
            frame.ability:SetText("" .. -1)
        elseif (event == "UNIT_HEALTH") then
            local health = GetPlayerHealth()
            local targetHealth = GetTargetHealth()
            frame.text:SetText("" .. health)
            frame.targetHealth:SetText("" .. targetHealth)
        elseif (event == "UNIT_MANA") then
            local mana = GetPlayerMana()
            frame.mana:SetText("" .. mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            frame.combat:SetText("0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            frame.combat:SetText("1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local tuid = UnitLevel("target")
            local targetHealth = GetTargetHealth()
            local distance = GetTargetDistance()
            frame.distance:SetText("" .. distance)
            frame.targetHealth:SetText("" .. targetHealth)
--            frame.tuid:SetText("TID: " .. tuid)
        elseif (event == "COMBAT_LOG_EVENT_UNFILTERED") then
            frame.ability:SetText("" .. GetSpellState())
        end
    end
)

frame:SetScript(
    "OnUpdate",
    function(self, event)
        local posX, posY = GetTruePosition()
        frame.posx:SetText("" .. string.sub(posX, 0, 8))
        frame.posy:SetText("" .. string.sub(posY, 0, 8))

        frame.facing:SetText("" .. string.sub(GetPlayerFacing(), 0, 8))

        frame.casting:SetText("" .. GetPlayerCastingState())
    end
)

function ShowFrame()
    frame:Show()
end
