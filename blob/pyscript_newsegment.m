fprintf(1,'Executing %s at %s:\n',mfilename(),datestr(now));
ver,
try,
        %% Generated by nipype.interfaces.spm
        if isempty(which('spm')),
             throw(MException('SPMCheck:NotFound', 'SPM not in matlab path'));
        end
        [name, version] = spm('ver');
        fprintf('SPM version: %s Release: %s\n',name, version);
        fprintf('SPM path: %s\n', which('spm'));
        spm('Defaults','fMRI');

        if strcmp(name, 'SPM8') || strcmp(name(1:5), 'SPM12'),
           spm_jobman('initcfg');
           spm_get_defaults('cmdline', 1);
        end

        jobs{1}.spm.spatial.preproc.channel(1).biasreg = 0.0001;
jobs{1}.spm.spatial.preproc.channel(1).write(1) = 1;
jobs{1}.spm.spatial.preproc.channel(1).write(2) = 1;
jobs{1}.spm.spatial.preproc.channel(1).biasfwhm = 60.0;
jobs{1}.spm.spatial.preproc.channel(1).vols = {...
'/nobackup/roggen2/Molloy/GluGABA/ZJ4T/ANATOMICAL/day7/ANATOMICAL.nii,1';...
};

        spm_jobman('run', jobs);

        
,catch ME,
fprintf(2,'MATLAB code threw an exception:\n');
fprintf(2,'%s\n',ME.message);
if length(ME.stack) ~= 0, fprintf(2,'File:%s\nName:%s\nLine:%d\n',ME.stack.file,ME.stack.name,ME.stack.line);, end;
end;