import { useState } from 'react';
import { deviceFrames } from '@/lib/mockData';
import { useProjectStore } from '@/stores/projectStore';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { 
  RotateCcw, 
  Camera, 
  Maximize2,
  Smartphone,
  Tablet,
  RefreshCw,
  Wifi,
  Battery,
  Signal
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function DevicePreview() {
  const [selectedDevice, setSelectedDevice] = useState(deviceFrames[0]);
  const [isLandscape, setIsLandscape] = useState(false);
  const { selectedFile, consoleLogs, addConsoleLog } = useProjectStore();

  const deviceWidth = isLandscape ? selectedDevice.height : selectedDevice.width;
  const deviceHeight = isLandscape ? selectedDevice.width : selectedDevice.height;
  const scale = Math.min(0.6, 350 / deviceWidth);

  const handleRefresh = () => {
    addConsoleLog({ type: 'info', message: 'Hot reload triggered' });
  };

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Toolbar */}
      <div className="h-12 border-b border-border bg-card flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Select
            value={selectedDevice.id}
            onValueChange={(id) => {
              const device = deviceFrames.find((d) => d.id === id);
              if (device) setSelectedDevice(device);
            }}
          >
            <SelectTrigger className="w-40 h-8">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {deviceFrames.map((device) => (
                <SelectItem key={device.id} value={device.id}>
                  <div className="flex items-center gap-2">
                    {device.type === 'phone' ? (
                      <Smartphone className="w-3 h-3" />
                    ) : (
                      <Tablet className="w-3 h-3" />
                    )}
                    {device.name}
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={() => setIsLandscape(!isLandscape)}
          >
            <RotateCcw className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={handleRefresh}
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Camera className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Maximize2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Device Frame */}
      <div className="flex-1 flex items-center justify-center p-8 overflow-auto">
        <div
          className="bg-foreground rounded-[3rem] p-3 shadow-2xl"
          style={{
            width: deviceWidth * scale + 24,
            height: deviceHeight * scale + 24,
          }}
        >
          {/* Device Screen */}
          <div
            className="bg-card rounded-[2.5rem] overflow-hidden relative"
            style={{
              width: deviceWidth * scale,
              height: deviceHeight * scale,
            }}
          >
            {/* Status Bar */}
            <div className="absolute top-0 left-0 right-0 h-6 bg-card/80 backdrop-blur flex items-center justify-between px-6 z-10">
              <span className="text-[10px] font-medium">9:41</span>
              <div className="flex items-center gap-1">
                <Signal className="w-3 h-3" />
                <Wifi className="w-3 h-3" />
                <Battery className="w-3 h-3" />
              </div>
            </div>

            {/* Dynamic Notch */}
            <div className="absolute top-2 left-1/2 -translate-x-1/2 w-24 h-6 bg-foreground rounded-full z-20" />

            {/* App Content */}
            <div className="h-full pt-8 flex flex-col">
              {/* App Bar */}
              <div className="bg-primary/20 px-4 py-3 flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-primary/30" />
                <span className="text-xs font-medium">Welcome</span>
              </div>

              {/* Body */}
              <div className="flex-1 flex flex-col items-center justify-center p-4 gap-3">
                <div className="w-16 h-16 rounded-2xl bg-primary/20 flex items-center justify-center">
                  <span className="text-2xl">🦋</span>
                </div>
                <span className="text-sm font-medium">Hello, FlutterAI!</span>
                <p className="text-[10px] text-muted-foreground text-center">
                  {selectedFile ? `Previewing: ${selectedFile.name}` : 'Your app preview appears here'}
                </p>
              </div>

              {/* Bottom Nav */}
              <div className="h-14 border-t border-border flex items-center justify-around px-4">
                {['🏠', '🔍', '❤️', '👤'].map((icon, i) => (
                  <div
                    key={i}
                    className={cn(
                      'w-10 h-10 rounded-full flex items-center justify-center',
                      i === 0 && 'bg-primary/20'
                    )}
                  >
                    <span className="text-sm">{icon}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Home Indicator */}
            <div className="absolute bottom-1 left-1/2 -translate-x-1/2 w-32 h-1 bg-foreground/50 rounded-full" />
          </div>
        </div>
      </div>

      {/* Console Panel */}
      <div className="h-32 border-t border-border bg-card">
        <div className="h-8 border-b border-border flex items-center px-4 justify-between">
          <span className="text-xs font-medium">Console</span>
          <span className="text-xs text-muted-foreground">{consoleLogs.length} logs</span>
        </div>
        <div className="h-24 overflow-auto p-2 font-mono text-xs space-y-1">
          {consoleLogs.slice(0, 10).map((log) => (
            <div
              key={log.id}
              className={cn(
                'flex items-start gap-2',
                log.type === 'error' && 'text-destructive',
                log.type === 'warning' && 'text-yellow-600',
                log.type === 'info' && 'text-muted-foreground'
              )}
            >
              <span className="opacity-50">
                {log.timestamp.toLocaleTimeString()}
              </span>
              <span>{log.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
